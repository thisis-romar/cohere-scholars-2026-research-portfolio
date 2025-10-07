# WhatsApp Receipt Processing System Overview

## Project Snapshot
- **Repository:** https://github.com/thisis-romar/emblem.io-whatsapp-receipts
- **Technology Stack:** Node.js 18+, Express.js, Google Document AI, Google Cloud Storage
- **Primary Goal:** Automate the ingestion of receipt images sent via WhatsApp and transform them into structured expense data ready for approval and export workflows.

## Feature Highlights
- **WhatsApp Business API Integration:** Ingests images and messages sent to a verified WhatsApp number.
- **OCR Pipeline:** Uses Google Document AI's expense processor to extract merchant details, totals, taxes, line items, and currencies from uploaded receipts.
- **Receipt Management:** Maintains a lifecycle for captured receipts including pending review, approval, rejection, and CSV export.
- **Interactive Messaging:** Sends confirmations, parsed receipt summaries, and guidance back to the user over WhatsApp.
- **Health & Monitoring:** Exposes heartbeat and status endpoints together with structured logging for observability.
- **Security & Safety:** Employs rate limiting, helmet-based headers, and optional webhook signature verification to mitigate abuse.

## System Requirements
### WhatsApp Platform
- Meta developer account with a WhatsApp Business App and connected phone number.
- Configured webhook URL plus a verify token shared between Meta and the application.
- Permanent or long-lived access token for authenticated API calls.

### Google Cloud Platform
- Enabled Document AI API within a billing-enabled Google Cloud project.
- Expense-specific Document AI processor ID (region defaults to `us-central1`).
- Service account JSON key with Document AI permissions stored at `config/gcp-service-account.json`.

### Local Development Setup
- Node.js v18 or newer with npm/yarn.
- `cp .env.template .env` to configure WhatsApp, Google Cloud, and server environment variables.
- Optional tooling: ngrok for webhook testing, Postman for manual API verification.

## Operational Workflow
1. **Inbound Message Handling**
   - Webhook endpoint (`/webhook/whatsapp`) verifies subscription challenges and receives inbound notifications from Meta.
   - Uploaded media is retrieved via WhatsApp APIs and temporarily stored in memory or local storage for processing.
2. **Receipt Processing**
   - Images are normalized with `sharp` prior to OCR submission.
   - Document AI returns structured expense entities that are transformed into internal receipt records.
3. **User Feedback & Storage**
   - Structured summaries are sent back to the originating WhatsApp conversation for confirmation.
   - Receipts persist with status flags to support approval workflows and exports.
4. **Administration & Export**
   - Approved receipts can be exported to CSV for downstream accounting or reimbursement pipelines.
   - Monitoring endpoints and logs provide operational insight for administrators.

## Running the Application
```bash
npm install
npm run dev        # nodemon for iterative development
npm start          # production start-up
```

### Useful Commands
```bash
# Webhook verification during setup
curl "http://localhost:3000/webhook/whatsapp?hub.mode=subscribe&hub.challenge=test&hub.verify_token=<token>"

# Local webhook tunnelling for testing
ngrok http 3000
```

## Testing & Quality
- Jest test suite with optional watch mode for rapid feedback.
- Playwright listed for potential end-to-end interface validation.
- ESLint and Prettier ensure consistent coding standards.

## Deployment Notes
- Includes Google Cloud Run deployment script (`npm run deploy`).
- Production build installs only runtime dependencies via `npm run build`.
- Supports horizontal scaling by remaining stateless; consider Redis for shared session state if needed.

## Security Considerations
- Built-in rate limiting (default 60 req/min) with IP level configuration.
- HTTPS enforcement recommended for webhook endpoints (ngrok during development).
- Receipt images processed in memory to minimize long-term sensitive data storage.

## Troubleshooting Tips
- **Webhook verification failures:** confirm `WEBHOOK_VERIFY_TOKEN` matches Meta configuration.
- **Document AI permission issues:** ensure the service account possesses `documentai.documents.process` rights.
- **Bot non-responsiveness:** validate webhook URL availability and check application logs.
- **Rate limit errors:** adjust rate limiting thresholds or add backoff logic for high-traffic scenarios.

## Scaling Guidance
- Deploy multiple stateless instances behind a load balancer for higher throughput.
- Monitor Document AI usage to manage cost per processed page.
- Cache frequently accessed metadata and use a CDN for static asset delivery if user interfaces are added.

## Related Resources
- [WhatsApp Business API Docs](https://developers.facebook.com/docs/whatsapp)
- [Google Document AI Documentation](https://cloud.google.com/document-ai/docs)
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)
- [Express.js Routing Guide](https://expressjs.com/en/guide/routing.html)

---
This summary captures the system capabilities and setup steps needed to evaluate or extend the WhatsApp receipt processing solution referenced above.
