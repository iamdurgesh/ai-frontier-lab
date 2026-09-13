# Security and privacy

Never commit credentials; .env is ignored and examples contain only empty/dummy values. Use least-privilege credentials. Never log secrets, prompts, submitted documents, or tool payloads. SecretStr masks settings representations but cannot protect values explicitly extracted by callers.

Use public, appropriately licensed or synthetic data by default. No employer material, confidential code, customer data, personal messages, or PII. External model APIs receive submitted content; document exactly what leaves the machine, the provider, retention considerations, and authorized purpose before a run.

Agent tools, including MCP tools, can execute arbitrary actions. Require explicit user consent and scoped authorization; maintain user control and approval for destructive actions. Treat tool descriptions, retrieved content, and MCP outputs as untrusted; test prompt injection and permission boundaries. Sandbox filesystem, processes, and network where possible. Review dependencies and downloaded code before execution.

Before any real deployment, record intended use, data flows, access controls, retention/deletion, and assess applicable GDPR/DSGVO and EU AI Act requirements using current authoritative sources. This repository makes no legal-compliance or production-readiness claim.

If a credential leaks, revoke/rotate it promptly and notify the repository owner through a private channel. Do not put secrets or sensitive reproduction details in public issues. No dedicated security contact or hosted reporting service is configured yet.
