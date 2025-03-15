# Azure OpenAI and Azure Search with azure.identity and autogen

During Y25H1 hackathon week, I set up my infrastructure removing any secret sharing and enabling RBAC. You can check out the details (https://github.com/sjyang18/ve-ai-sfi-infra). The next logical step was figuring out how to connect these resources and run queries against my data. I began by converting some materials from my AI training to using azure.identity. Then, I converted LangChain to Autogen to interact with data and OpenAI. My learnings are experiemented & documented in module-2.


## Development instructions

## With devcontainer

This repository comes with a devcontainer (a Dockerized Python environment). If you open it in Codespaces, it should automatically initialize the devcontainer.

Locally, you can open it in VS Code with the Dev Containers extension installed.

## Without devcontainer

If you can't or don't want to use the devcontainer, then you should first create a virtual environment:

```
python3 -m venv .venv
source .venv/bin/activate
```

Then install the dev tools and pre-commit hooks:

```
python3 -m pip install --user -r requirements-dev.txt
pre-commit install
```
