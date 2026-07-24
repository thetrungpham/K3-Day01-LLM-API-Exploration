import tkinter as tk
from tkinter import ttk, scrolledtext
import threading

from template import (
    call_openai,
    call_openai_mini,
    count_tokens,
    estimate_cost,
)

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700


class ChatGUI:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("OpenAI Chatbot")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        self.history = []

        self.build_top()

        self.build_chat()

        self.build_bottom()

        self.build_status()
        self.add_menu()

    def build_top(self):

        frame = ttk.Frame(self.root)
        frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame, text="Model").grid(row=0, column=0)

        self.model_var = tk.StringVar(value="gpt-4o-mini")

        self.model_box = ttk.Combobox(
            frame,
            textvariable=self.model_var,
            values=[
                "gpt-4o",
                "gpt-4o-mini",
            ],
            width=20,
            state="readonly",
        )

        self.model_box.grid(row=0, column=1, padx=5)

        ttk.Label(frame, text="Temperature").grid(row=0, column=2)

        self.temp_var = tk.DoubleVar(value=0.7)

        self.temp_scale = tk.Scale(
            frame,
            variable=self.temp_var,
            from_=0,
            to=2,
            resolution=0.1,
            orient="horizontal",
            length=250,
        )

        self.temp_scale.grid(row=0, column=3, padx=5)

    def build_chat(self):

        self.chat = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            font=("Consolas", 11),
            state="disabled",
        )

        self.chat.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10,
        )

    def build_bottom(self):

        frame = ttk.Frame(self.root)
        frame.pack(fill="x", padx=10, pady=5)

        self.input_box = tk.Text(
            frame,
            height=4,
            font=("Consolas", 11),
        )

        self.input_box.pack(
            side="left",
            fill="x",
            expand=True,
        )

        self.input_box.bind("<Return>", self.enter_send)

        self.send_btn = ttk.Button(
            frame,
            text="Send",
            command=self.send_message,
            width=15,
        )

        self.send_btn.pack(
            side="right",
            padx=5,
        )

    def build_status(self):

        frame = ttk.Frame(self.root)
        frame.pack(fill="x", padx=10)

        self.status = tk.StringVar()

        self.status.set("Ready")

        ttk.Label(
            frame,
            textvariable=self.status,
        ).pack(anchor="w")
    def enter_send(self, event):

        if event.state == 0:
            self.send_message()
            return "break"

    def append(self, sender, message):

        self.chat.config(state="normal")

        self.chat.insert(tk.END, f"{sender}\n", "title")
        self.chat.insert(tk.END, message + "\n\n")

        self.chat.tag_config(
            "title",
            foreground="blue",
            font=("Consolas", 11, "bold"),
        )

        self.chat.config(state="disabled")

        self.chat.see(tk.END)

    def send_message(self):

        prompt = self.input_box.get("1.0", tk.END).strip()

        if not prompt:
            return

        self.input_box.delete("1.0", tk.END)

        self.append("You", prompt)

        self.send_btn.config(state="disabled")

        self.status.set("Waiting for OpenAI...")

        threading.Thread(
            target=self.ask_openai,
            args=(prompt,),
            daemon=True,
        ).start()

    def ask_openai(self, prompt):

        model = self.model_var.get()

        temperature = self.temp_var.get()

        try:

            if model == "gpt-4o":

                response, latency = call_openai(
                    prompt=prompt,
                    temperature=temperature,
                )

            else:

                response, latency = call_openai_mini(
                    prompt=prompt,
                    temperature=temperature,
                )

            input_tokens = count_tokens(prompt, model)

            output_tokens = count_tokens(response, model)

            cost = estimate_cost(
                model=model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
            )

            self.root.after(
                0,
                lambda: self.finish_response(
                    response,
                    latency,
                    input_tokens,
                    output_tokens,
                    cost,
                ),
            )

        except Exception as e:

            error_msg = str(e)

            self.root.after(
                0,
                lambda: self.show_error(error_msg),
            )

    def finish_response(
        self,
        response,
        latency,
        input_tokens,
        output_tokens,
        cost,
    ):

        self.append("Assistant", response)

        self.status.set(
            f"Latency: {latency:.2f}s | "
            f"Input: {input_tokens} | "
            f"Output: {output_tokens} | "
            f"Cost: ${cost:.6f}"
        )

        self.send_btn.config(state="normal")

    def show_error(self, text):

        self.append("Error", text)

        self.status.set("Failed")

        self.send_btn.config(state="normal")

        # -----------------------------
    # Menu
    # -----------------------------
    def add_menu(self):

        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(
            menubar,
            tearoff=False,
        )

        file_menu.add_command(
            label="Clear Chat",
            command=self.clear_chat,
        )

        file_menu.add_command(
            label="Save Chat",
            command=self.save_chat,
        )

        file_menu.add_separator()

        file_menu.add_command(
            label="Exit",
            command=self.root.destroy,
        )

        menubar.add_cascade(
            label="File",
            menu=file_menu,
        )

        self.root.config(menu=menubar)

    # -----------------------------
    # Clear chat
    # -----------------------------
    def clear_chat(self):

        self.chat.config(state="normal")
        self.chat.delete("1.0", tk.END)
        self.chat.config(state="disabled")

        self.status.set("Ready")

    # -----------------------------
    # Save conversation
    # -----------------------------
    def save_chat(self):

        text = self.chat.get("1.0", tk.END)

        with open(
            "conversation.txt",
            "w",
            encoding="utf8",
        ) as f:

            f.write(text)

        self.status.set("Saved to conversation.txt")

    # -----------------------------
    # Run
    # -----------------------------
    def run(self):


        self.root.mainloop()


if __name__ == "__main__":

    app = ChatGUI()

    app.run()