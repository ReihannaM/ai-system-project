# AI Features Setup Guide

## Quick Start: Enable AI in 3 Steps

### Step 1: Get an API Key (Free)

1. Visit https://console.anthropic.com
2. Click "Sign Up"
3. Create a free account
4. Generate an API key
5. Copy the key (starts with `sk-ant-`)

### Step 2: Set Environment Variable

**macOS/Linux:**
```bash
export ANTHROPIC_API_KEY='sk-ant-...'
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY='sk-ant-...'
```

**Windows (Command Prompt):**
```cmd
set ANTHROPIC_API_KEY=sk-ant-...
```

**Permanent (macOS/Linux):**
```bash
# Add to ~/.zprofile or ~/.bashrc
echo "export ANTHROPIC_API_KEY='sk-ant-...'" >> ~/.zprofile
source ~/.zprofile
```

### Step 3: Install & Run

```bash
# Install dependencies (if not already done)
pip install -r requirements.txt

# Run the app
streamlit run vet_app.py

# Navigate to 🤖 AI Assistant tab
```

## Verify Installation

The app will show:
- ✅ AI Assistant Status: GREEN (Available)
- ✅ All AI features enabled
- ✅ Ready to use

If you see ⚠️ warnings instead, check:
1. API key is set correctly
2. Key hasn't been copied wrong
3. No extra spaces at beginning/end
4. Using backticks: `export ANTHROPIC_API_KEY='key'`

## What AI Can Do

Once enabled, you get:

### 1. **Symptom Analysis** 🔍
- Input symptoms → Get possible diagnoses
- Based on patient history
- Includes test recommendations

### 2. **Auto-Generate Notes** 📝
- Describe observations
- AI creates professional SOAP notes
- Ready for medical records

### 3. **Drug Interaction Check** 💊
- New medication → Check safety
- Reviews current drugs
- Alerts on allergies

### 4. **Follow-up Planner** 📅
- Past treatment → Future care plan
- Timeline recommendations
- Home care instructions

### 5. **Cost Estimator** 💰
- Select treatments
- AI estimates based on clinic cases
- Helps client communication

## Cost Examples

**Typical Monthly Usage** (20 features/month):
- Symptom analyses: 5 × $0.01 = $0.05
- Generated notes: 5 × $0.01 = $0.05
- Drug checks: 5 × $0.01 = $0.05
- Follow-up plans: 3 × $0.01 = $0.03
- Cost estimates: 2 × $0.01 = $0.02

**Total: ~$0.20/month** (Free for first 5M tokens)

## Logging

AI operations are automatically logged:
```
INFO - AI Assistant initialized
INFO - Retrieved medical history for Max
INFO - Symptom analysis complete
INFO - Drug interaction check complete
```

Useful for:
- Tracking AI usage
- Debugging issues
- Audit compliance
- Billing verification

## Security Notes

✅ **DO:**
- Keep API key secret
- Don't commit to GitHub
- Use environment variables
- Rotate keys periodically

❌ **DON'T:**
- Paste key in code
- Share key in emails
- Put in version control
- Expose in logs

## Troubleshooting

### Issue: "AI Assistant Not Configured"

**Check:**
```bash
# Verify environment variable is set
echo $ANTHROPIC_API_KEY
# Should show your key (or nothing if not set)
```

**Fix:**
```bash
export ANTHROPIC_API_KEY='sk-ant-...'
streamlit run vet_app.py
```

### Issue: "API Error" or Connection Failed

**Check:**
1. Internet connection active
2. API key valid (test at console.anthropic.com)
3. API not rate limited
4. No firewall blocking requests

**Debug:**
```python
# Test API connection
from anthropic import Anthropic
client = Anthropic(api_key='sk-ant-...')
msg = client.messages.create(model="claude-3-5-sonnet-20241022", max_tokens=10, messages=[{"role": "user", "content": "Hi"}])
print(msg.content[0].text)
```

Should show a response without error.

### Issue: Recommendations Don't Make Sense

**Check:**
1. Patient data complete (history, meds, allergies)
2. Symptom description detailed
3. Medical records up-to-date

**Fix:**
- Add more context
- Review patient history
- Ensure data accuracy

## Testing AI Features

### Test Symptom Analysis

1. Go to **AI Assistant** → **Symptom Analysis**
2. Select any animal (or use test data)
3. Enter symptom: "Lethargy and loss of appetite"
4. Click "Analyze Symptoms"

Expected: AI suggests conditions based on animal's history

### Test Drug Interactions

1. Go to **Drug Interactions**
2. Select an animal
3. Enter medication: "Amoxicillin"
4. Dosage: "500mg twice daily"
5. Click "Check Interactions"

Expected: AI checks against current meds

### Test Cost Estimation

1. Go to **Cost Estimation**
2. Select an animal
3. Check treatments: Vaccination, Exam
4. Click "Estimate Costs"

Expected: AI calculates estimate

## Next Steps

Once AI is working:

1. **Try all features** - See how each one helps
2. **Check recommendations** - Verify accuracy for your cases
3. **Integrate into workflow** - Use daily for case support
4. **Give feedback** - Note useful/not useful recommendations
5. **Customize** - Adjust confidence thresholds if needed

## Advanced Configuration

### Adjust Model (Optional)

Default uses Claude 3.5 Sonnet (best balance of speed/accuracy).

To use different model:
```python
# In vet_ai_assistant.py
self.model = "claude-3-opus-20250219"  # More capable, slower
# or
self.model = "claude-3-haiku-20250307"  # Faster, lower cost
```

### Modify RAG Behavior

Increase cache size for faster retrieval:
```python
# In vet_office_system.py
self.rag_cache = {}  # Increased from default

# In vet_ai_assistant.py
self.rag_cache_ttl = 3600  # 1 hour cache
```

## FAQ

**Q: Can I use AI without paying?**
A: Yes! Anthropic offers free tier with 5M input tokens/month.

**Q: Will data be kept by Anthropic?**
A: No - API calls are not used for training. See https://www.anthropic.com/privacy

**Q: Can I use other AI models?**
A: Yes - modify `vet_ai_assistant.py` to use different providers

**Q: How accurate is the AI?**
A: Depends on data quality. Verified + tested better than untested.

**Q: What if AI is wrong?**
A: That's why it's "decision support" - always verify with diagnostics

## Going Live

Before using with real patients:

✅ Test with sample cases
✅ Verify accuracy for your cases
✅ Train staff on AI features
✅ Set up logging/audit trail
✅ Document in clinic SOP
✅ Update client consent forms (optional)
✅ Have vet review all recommendations

## Support

- **Docs**: See [VET_AI_GUIDE.md](VET_AI_GUIDE.md)
- **Code**: `vet_ai_assistant.py` - source code
- **Logs**: Enable debug logging for details
- **Help**: Check error messages - usually very clear

---

**Ready to empower your vet clinic with AI!** 🚀

Questions? Check the main documentation or logs.
