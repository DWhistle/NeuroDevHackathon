# Security remediation

The original commit contained an upstream neuro-platform JWT in `model_builder.py`
and shared MySQL login credentials plus a public database address in `server.js`,
`socketManager.js`, and the archived file `4`. Their values are intentionally omitted.

Current code reads database settings and service endpoints from environment
variables (`.env.example`). The unreachable experimental upstream HTTP/JWT block
was removed; `NEURO_API_TOKEN` is a reserved environment setting if that acquisition
client is implemented later. No active code uses an upstream token.

1. Revoke the exposed JWT and issue a new token through the original provider.
   Its present validity is unknown; this cleanup never attempts authentication.
2. Rotate the exposed MySQL password and any reused credentials. Revoke unused
   accounts and replace broad database privileges with a dedicated local account.
3. Review provider/database access logs and restrict network access. These
   unauthenticated prototype HTTP, Socket.IO, and RPC services are for isolated
   local experiments. They do not implement TLS, access control, or safe public
   operation. HTTP listeners currently bind all interfaces.
4. Old commits still contain the exposed material. An owner must separately plan
   history cleanup, coordinate forks/clones and cached copies with collaborators
   and GitHub, and verify remediation afterwards. Rotation comes first. This PR
   does not rewrite history or force-push.
5. Review provenance and publication consent for the existing `PythonStash/*.csv`
   recordings before using them in public demonstrations. Consent, source,
   anonymization, and redistribution rights are not documented in the original
   repository. This PR preserves those existing files and never uses them for
   tests or generates new private-source examples. Notebook rendered outputs
   were cleared; the source cells remain.

Checks for literal credentials are scoped inspections, not a full security audit.
The historical dependency stack needs a separate dependency/security review before
any network deployment. Do not put real secrets into `.env.example`, logs, issues,
PRs, or commits; `.env` is ignored.
