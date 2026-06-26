# Agent Roles

## Hermes

Current Feishu entrypoint. It receives user instructions and sends them to
`SPIS-Orchestrator`. Hermes should not write SPIS business tables directly.

## SPIS-Orchestrator

Small FastAPI service. It creates task records, decides which agents run, calls model
providers, stores results, and returns status to Hermes or Feishu.

## DeepSeek Coding Agent

Primary coding and repair model. It should produce plans, patches, tests, and fix
suggestions. Later it can be connected to a GitHub branch worker.

## OpenAI Review Agent

Final reviewer. It checks architecture, bugs, test gaps, security, traceability,
rollback, and whether human approval is required.

## Doubao Business Agent

Chinese procurement and fastener-domain assistant. It turns supplier prices, MOQ,
discounts, BOM, and quotation rules into structured requirements.

## Orange Pi Worker

Second phase. Use it for test/build/preview jobs and price collection. It should call
the orchestrator over a private network or pull tasks from a queue later.
