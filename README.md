# 🤖 DeepChat

[![author](https://img.shields.io/badge/author-mohd--faizy-red)](https://github.com/mohd-faizy)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Ollama](https://img.shields.io/badge/Ollama-0C0D0E?logo=ollama&logoColor=white)](https://ollama.ai)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://python.org)

DeepChat is an AI-powered chatbot leveraging `DeepSeek-R1` (1.5B) parameters, built with `Streamlit` and `Ollama` for seamless and interactive conversations.

![Demo](https://github.com/mohd-faizy/DeepChat/blob/main/assets/deepChat.png?raw=true)

## Directory Structure

```
deepchat/
├── app/
│   ├── __init__.py
│   ├── main.py          # Streamlit application
│   └── utils.py         # Helper functions
├── assets              
├── requirements.txt     # Python dependencies
├── .gitignore
├── README.md            
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- [Ollama](https://ollama.ai/) installed and running
- DeepSeek-R1 model:

  ```bash
  ollama pull deepseek-r1:1.5b
  ```

### Installation

1. Clone repository:

   ```bash
   git clone https://github.com/your-username/deepchat.git
   cd deepchat
   ```

2. Create virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate environment:

   ```bash
   # Linux/macOS
   source venv/bin/activate
   
   # Windows
   .\venv\Scripts\activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### 🖥️ Usage

1. Start Ollama service:

   ```bash
   ollama serve
   ```

2. In a separate terminal, launch the chat interface:

   ```bash
   streamlit run app/main.py
   ```


## 🔧 Troubleshooting

**Port Conflict (11434):**

```bash
# Windows
netstat -ano | findstr :11434
taskkill /PID <PID> /F

# Linux/macOS
lsof -i :11434
kill -9 <PID>
```

**Common Issues:**

- Ensure Ollama is running before launching the Streamlit app
- Verify model installation: `ollama list`
- Check firewall settings if experiencing connection issues


## 🍰 Contributing

Contributions are welcome!

## ⚖ ➤ License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## ❤️ Support

If you find this repository helpful, show your support by starring it! For questions or feedback, reach out on [Twitter(`X`)](https://twitter.com/F4izy).

## 🔗Connect with me

➤ If you have questions or feedback, feel free to reach out!!!

[<img align="left" src="https://cdn4.iconfinder.com/data/icons/social-media-icons-the-circle-set/48/twitter_circle-512.png" width="32px"/>][twitter]
[<img align="left" src="https://cdn-icons-png.flaticon.com/512/145/145807.png" width="32px"/>][linkedin]
[<img align="left" src="https://cdn-icons-png.flaticon.com/512/2626/2626299.png" width="32px"/>][Portfolio]

[twitter]: https://twitter.com/F4izy
[linkedin]: https://www.linkedin.com/in/mohd-faizy/
[Portfolio]: https://ai.stackexchange.com/users/36737/faizy?tab=profile

---

<img src="https://github-readme-stats.vercel.app/api?username=mohd-faizy&show_icons=true" width=380px height=200px />
