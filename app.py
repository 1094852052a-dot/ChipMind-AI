import json
from datetime import datetime
import streamlit as st

from core.config import OLLAMA_MODEL, OPENAI_MODEL, OPENAI_API_KEY
from core.router import ask_ollama, ask_openai, check_ollama

st.set_page_config(
    page_title="ChipMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.block-container {padding-top: 2rem; max-width: 1200px;}
.main-title {font-size: 2.2rem; font-weight: 750; letter-spacing: -1px;}
.sub-title {color: #8b949e; margin-top: -8px;}
[data-testid="stChatMessage"] {border-radius: 12px;}
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown('<div class="main-title">🧠 ChipMind AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Electronic Components Intelligence Workbench · V1.0</div>', unsafe_allow_html=True)
st.write("你的电子元器件销售与技术辅助工作台。默认优先使用本地模型。")

with st.sidebar:
    st.header("⚙️ 模型设置")
    provider = st.radio("模型运行方式", ["本地 Ollama", "云端 OpenAI"], index=0)
    if provider == "本地 Ollama":
        model = st.text_input("Ollama 模型名称", value=OLLAMA_MODEL)
        if st.button("检测本地模型连接", use_container_width=True):
            try:
                models = check_ollama()
                st.success("Ollama 连接成功")
                if models:
                    st.caption("已安装模型：" + "、".join(models))
                else:
                    st.warning("服务可连接，但尚未发现已安装模型。")
            except Exception as exc:
                st.error(f"连接失败：{exc}")
    else:
        model = st.text_input("OpenAI 模型名称", value=OPENAI_MODEL)
        if OPENAI_API_KEY:
            st.success("已检测到 API Key")
        else:
            st.warning("尚未配置 OPENAI_API_KEY，请编辑 .env 文件。")

    st.divider()
    st.caption("本地模式的数据请求发送到本机 Ollama。云端模式会将对话内容发送给云端模型服务。")
    if st.button("清空当前对话", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.session_state.messages:
        export_text = "# ChipMind AI 对话记录\\n\\n"
        for msg in st.session_state.messages:
            role = "用户" if msg["role"] == "user" else "ChipMind AI"
            export_text += f"## {role}\\n\\n{msg['content']}\\n\\n"
        st.download_button(
            "导出对话 Markdown",
            data=export_text,
            file_name=f"chipmind_chat_{datetime.now():%Y%m%d_%H%M}.md",
            mime="text/markdown",
            use_container_width=True
        )

# Quick-start prompts
if not st.session_state.messages:
    st.subheader("可以这样开始")
    prompts = [
        "帮我分析 LM5066IPMHX 的主要功能、关键参数和选型注意事项。",
        "客户需要一颗 RS-485 收发器，我应该先向客户确认哪些信息？",
        "帮我设计一套工业控制客户的元器件销售跟进流程。",
        "分析芯片替代料时，必须核对哪些参数？"
    ]
    cols = st.columns(2)
    for idx, prompt in enumerate(prompts):
        if cols[idx % 2].button(prompt, key=f"quick_{idx}", use_container_width=True):
            st.session_state.pending_prompt = prompt
            st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("输入芯片型号、客户需求或业务问题……")
if not prompt and st.session_state.get("pending_prompt"):
    prompt = st.session_state.pop("pending_prompt")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("ChipMind AI 正在思考……"):
            try:
                history = st.session_state.messages[:-1]
                if provider == "本地 Ollama":
                    answer = ask_ollama(history + [{"role": "user", "content": prompt}], model=model)
                else:
                    answer = ask_openai(history + [{"role": "user", "content": prompt}], model=model)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as exc:
                error = f"调用失败：{exc}"
                st.error(error)
                st.info("请检查模型服务、模型名称、网络连接和 API 配置。")
