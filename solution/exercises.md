# K3 — Ngày 1: Bài Tập & Phản Ánh
## Khám Phá LLM API | Phiếu Thực Hành

**Thời lượng:** 9h00–13h00
**Cách làm:** Trả lời từng câu ngay sau khi hoàn thành block tương ứng —
đừng để dồn hết về cuối buổi. Thay dòng `*Câu trả lời của bạn*` bằng câu
trả lời thật (chấm tự động sẽ đếm số câu đã trả lời).

---

## Block 1 — API Cơ Bản (trả lời sau Checkpoint 1)

### Câu 1.1 — Độ nhạy của temperature
Gọi `call_openai` với temperature 0.0, 0.5, 1.0 và 1.5 dùng prompt
**"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> Khi temperature tăng, phản hồi càng trở nên đa dạng và sáng tạo hơn, có nhiều nội dung mới. Ở temperature thấp, câu trả lời chặt chẽ hơn, ít biến đổi và chính xác hơn.

### Câu 1.2 — Chọn temperature cho sản phẩm
**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> Mình sẽ ưu tiên temperature thấp để có độ chính xác cao cho khách hàng còn đặt là bao nhiêu thì phải phụ thuộc từng domain.

### Câu 1.3 — Đánh đổi chi phí
Kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người gọi API 3 lần,
mỗi lần trung bình ~350 token đầu ra.

**Ước tính GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này? Nêu một
trường hợp GPT-4o xứng đáng với chi phí và một trường hợp nên dùng mini:**
> GPT-4o đắt hơn khoảng 16.7 lần đối với token đầu ra.
> GPT-4o phù hợp khi cần phân tích chuyên sâu hoặc chất lượng cao.
> GPT-4o-mini phù hợp cho FAQ và chatbot hỗ trợ khách hàng.

---

## Block 2 — System Prompt & Token (trả lời sau Checkpoint 2)

### Câu 2.1 — Sức mạnh của persona
Gọi `chat_with_system_prompt` hai lần với cùng câu hỏi
**"Giải thích blockchain là gì?"** nhưng hai system prompt khác nhau:
- "Bạn là giáo viên tiểu học, giải thích thật đơn giản cho trẻ 8 tuổi."
- "Bạn là chuyên gia tài chính, trả lời chuyên sâu bằng thuật ngữ kỹ thuật."

**Hai phản hồi khác nhau như thế nào (độ dài, từ vựng, ví dụ)? System prompt
ảnh hưởng đến hành vi model ra sao?** (3–4 câu)
> Phiên bản giáo viên tiểu học trả lời ngắn gọn, đơn giản, dùng ví dụ dễ hiểu. Phiên bản chuyên gia tài chính nói dài hơn, dùng thuật ngữ chuyên môn hơn. System prompt làm model theo đúng vai trò  chỉ định.

### Câu 2.2 — tiktoken vs đếm từ
Chọn một đoạn văn tiếng Việt ~100 từ. So sánh số token theo `count_tokens`
(tiktoken) với ước lượng `số từ / 0.75` mà Part 1 đã dùng.

**Hai con số chênh nhau bao nhiêu phần trăm? Vì sao tiếng Việt thường tốn
nhiều token hơn tiếng Anh cùng độ dài?**
> Ví dụ tiktoken có thể cho tầm 120 token còn ước lượng /0.75 là 133 token gì đó, chênh khoảng 10–15%. Tiếng Việt thường nhiều token hơn vì dấu câu, dấu chữ và cách mã hóa subword khiến một số từ có thể bị tách thành nhiều token hơn.

---

## Block 3 — Streaming & Độ Bền (trả lời sau Checkpoint 3)

### Câu 3.1 — Trải nghiệm người dùng với streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì
non-streaming lại phù hợp hơn?** (1 đoạn văn)
> Streaming quan trọng khi cần phản hồi nhanh theo thời gian thực, ví dụ chat tương tác hoặc giao diện người dùng mong đợi trả lời từng phần. Non-streaming phù hợp hơn khi cần đầu ra hoàn chỉnh và kiểm soát lỗi dễ hơn, như tạo báo cáo hay xử lý batch.

### Câu 3.2 — Vì sao backoff theo cấp số nhân?
**So với delay cố định (ví dụ luôn chờ 1 giây), exponential backoff có lợi
thế gì khi API bị quá tải? Điều gì xảy ra nếu hàng nghìn client cùng retry
với delay cố định giống nhau?**
> Exponential backoff giảm tải tự nhiên bằng cách tăng thời gian chờ sau mỗi lần thất bại. Nếu hàng nghìn client retry cùng delay cố định, sẽ xảy ra đợt retry đồng loạt và làm quá tải API hơn nữa. Backoff giúp tránh bão retry và cho hệ thống hồi phục ổn định.

---

## Block 4 — Mini-Project (trả lời sau Checkpoint 4)

### Câu 4.1 — Thiết kế persona
**Bạn chọn persona gì cho trợ lý của mình? Viết lại system prompt đó và giải
thích 1–2 lựa chọn từ ngữ quan trọng trong prompt (ví dụ: vì sao yêu cầu
"trả lời ngắn gọn", vì sao chỉ định ngôn ngữ...):**
> Persona: "Bạn là trợ lý học tập thân thiện, trả lời ngắn gọn bằng tiếng Việt, dễ hiểu và chuyên tâm vào câu hỏi." Yêu cầu "trả lời ngắn gọn" giúp tránh phản hồi dài dòng. Chỉ định tiếng Việt đảm bảo trợ lý sử dụng ngôn ngữ phù hợp với người dùng.

### Câu 4.2 — Hạn chế & cải thiện
**Trợ lý của bạn hiện có hạn chế lớn nhất là gì (ví dụ: history chỉ 3 lượt,
không có bộ nhớ dài hạn, không kiểm duyệt nội dung...)? Đề xuất một cải
thiện cụ thể và mô tả ngắn cách triển khai:**
> Hạn chế lớn nhất là không có bộ nhớ dài hạn và chỉ giữ 3 lượt history. Cải thiện bằng cách lưu tóm tắt vào bộ nhớ ngoài và thêm summary đó vào system prompt khi khởi đầu phiên sau. 

---

## Danh Sách Kiểm Tra Nộp Bài

- [ ] `python grade.py` — xem điểm tự động, mục tiêu ≥ 75/100
- [ ] Cả 4 checkpoint pytest đều pass
- [ ] Tất cả 9 câu trong file này đã được trả lời
- [ ] Đã copy bài làm vào folder `solution/` và zip theo hướng dẫn README
