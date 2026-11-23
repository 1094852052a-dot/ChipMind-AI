# ChipMind AI

面向电子元器件销售、采购与技术支持的本地 AI 工作台。V1.0 提供本地 Ollama / 云端 OpenAI 双模型对话、模型连通性检测、会话记录导出，以及面向芯片业务的系统提示词。

## 主要特性

- **双模型路由**：选择 Ollama 本地模型或 OpenAI 云端模型。
- **本地优先**：默认使用 Ollama；本地资料无需上传云端。
- **芯片销售助手**：内置电子元器件销售场景提示词。
- **网页界面**：Streamlit 本地网页应用。
- **安全配置**：API Key 放在 `.env`，不写入代码仓库。

> 当前版本是可运行的 V1.0 对话工作台。芯片型号联网检索、Datasheet 解析、BOM 分析、客户 CRM 将在后续版本增加。模型回答不能替代原厂 Datasheet、授权渠道和实物检测。

## 技术栈

- Python 3.11+
- Streamlit
- Ollama
- OpenAI Python SDK

## Windows 11 安装

### 1. 准备 Ollama

安装 Ollama： https://ollama.com/download

打开 PowerShell，拉取一个适合 24GB 显存的模型，例如：

```powershell
ollama pull qwen2.5:14b
```

启动/确认 Ollama 服务：

```powershell
ollama serve
```

如果 Ollama 已作为 Windows 后台服务运行，通常无需重复执行。默认地址为 `http://localhost:11434`。

### 2. 安装项目

解压项目后，在 PowerShell 进入项目目录：

```powershell
cd ChipMind-AI
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

如果 PowerShell 阻止激活脚本，可在当前窗口执行：

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env`：

```powershell
Copy-Item .env.example .env
```

默认不需要 OpenAI Key 就能使用 Ollama。若要使用云端模型，在 `.env` 中填写：

```env
OPENAI_API_KEY=你的_API_Key
OPENAI_MODEL=gpt-4.1-mini
```

请勿把 `.env` 上传到 GitHub。

### 4. 启动

```powershell
streamlit run app.py
```

浏览器访问：

```text
http://localhost:8501
```

## 使用说明

1. 左侧选择“本地 Ollama”或“云端 OpenAI”。
2. 本地模式填写已通过 `ollama list` 安装的模型名称，例如 `qwen2.5:14b`。
3. 云端模式需要在 `.env` 配置 `OPENAI_API_KEY`。
4. 输入芯片型号、客户需求或销售场景问题，点击发送。
5. 可将当前对话导出为 Markdown。

## 常见问题

### Ollama 连接失败
- 确认 Ollama 已安装并运行。
- 浏览器本身不直接连接 Ollama，Streamlit 后端会请求 `http://localhost:11434`。
- 在 PowerShell 执行 `ollama list` 检查模型是否存在。
- 如果修改了 Ollama 端口，请在 `.env` 修改 `OLLAMA_BASE_URL`。

### 模型名称不存在
执行 `ollama list` 查看准确名称，复制到左侧模型输入框。

### OpenAI 模式报错
检查 `.env` 中 `OPENAI_API_KEY` 是否正确，并确认账户/API 项目有可用额度及模型访问权限。

## 项目结构

```text
ChipMind-AI/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── core/
│   ├── __init__.py
│   ├── config.py
│   ├── prompts.py
│   └── router.py
└── docs/
    └── ROADMAP.md
```

## 安全建议

- 不要把客户名称、报价、合同、个人信息或商业机密发送到云端模型，除非已获得授权并确认符合公司政策。
- API Key 仅保存在本机 `.env`。
- 模型生成的封装、引脚、绝对最大额定值、替代料和库存价格必须回到原厂资料或可信供应商处核实。

## License

MIT
