# Stock Portfolio Suggestion Engine — Test Cases for Graders


### Prerequisites

- Python **3.8 or newer**
- Active **internet** connection (live prices from Yahoo Finance via `yfinance`)
- macOS / Windows / Linux terminal

### Install dependencies

1. Unzip the project and open a terminal in the project root (folder containing `main.py`, `app.py`, `requirements.txt`).
2. (Recommended) Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate          # macOS/Linux
   # venv\Scripts\activate           # Windows
   ```
3. Install packages (use `python3 -m pip` if `pip` is not found):
   ```bash
   python3 -m pip install -r requirements.txt
   ```

### Two ways to run the app

| Interface | Start command | How to interact |
|-----------|---------------|-----------------|
| **CLI** | `python main.py` | Answer prompts in the terminal |
| **Web UI** | `python app.py` then open `http://127.0.0.1:5001` | Form + “Generate Portfolio” button |

Unless a test case says **Web only** or **CLI only**, you may use either interface; expected results are the same.

### Optional: run the same 10 cases with pytest (automated)

The repository includes automated tests that mirror these manual cases (offline, no live market data):

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m pytest -v
```

Each pytest function is named `test_case_XX_...` to match **Test Case 1–10** above. 

Optional live Yahoo Finance check (needs network):

```bash
python3 -m pytest -m integration -v
```

---

## Test Case 1 — Welcome and strategy list (CLI)

**Goal:** Verify the CLI starts and lists all five strategies with at least three securities each.

**Steps:**

1. From project root: `python main.py`
2. Read the welcome banner.
3. When prompted for investment amount, press `Ctrl+C` to exit (no portfolio needed).

**Expected results:**

- Title **“STOCK PORTFOLIO SUGGESTION ENGINE”** appears.
- All five strategies are listed with descriptions and tickers:
  - Ethical Investing — includes **AAPL, ADBE, NSRGY** (and others)
  - Growth Investing — includes **TSLA, NVDA, AMD** (and others)
  - Index Investing — includes **VTI, IXUS, ILTB**
  - Quality Investing — includes **JNJ, KO, PG** (and others)
  - Value Investing — includes **BAC, F, XOM** (and others)
- Each strategy shows **at least 3** ticker symbols.

---

## Test Case 2 — Reject investment below $5,000 (CLI)

**Goal:** Enforce minimum investment of **$5,000 USD**.

**Steps:**

1. Run `python main.py`
2. At **“Enter investment amount”**, enter: `4999`
3. When rejected, enter: `5000` and continue (any valid strategy selection is fine for the rest of this case; you may exit with `Ctrl+C` after amount is accepted).

**Expected results:**

- For `4999`: error message stating minimum is **$5,000**; prompt repeats.
- For `5000`: amount is accepted; flow continues to strategy selection.

---

## Test Case 3 — Reject investment below $5,000 (Web UI)

**Goal:** Same minimum rule on the web interface.

**Steps:**

1. Run `python app.py`
2. Open `http://127.0.0.1:5001` in a browser.
3. Click **one** strategy card (e.g. Index Investing).
4. Enter amount: `1000`
5. Click **Generate Portfolio**

**Expected results:**

- Red error: investment must be at least **$5,000**
- Results panel does **not** show holdings.

---

## Test Case 4 — Single strategy: Index Investing ($10,000)

**Goal:** Map Index strategy to specified ETFs, show allocation and live portfolio value.

**Steps (CLI):**

1. `python main.py`
2. Amount: `10000`
3. Strategies: `index` or `3`
4. Wait for price fetch and portfolio output.

**Steps (Web — alternative):**

1. `python app.py` → `http://127.0.0.1:5001`
2. Amount: `10000`
3. Select **Index Investing** only → **Generate Portfolio**

**Expected results:**

- Selected holdings include exactly these ETFs: **VTI, IXUS, ILTB** (no other tickers for this run).
- **PORTFOLIO ALLOCATION** / results show:
  - Total investment **$10,000.00**
  - Per-ticker: shares, price, position value
  - **Current Portfolio Value** (sum of positions; may differ slightly from $10,000 due to fractional shares and live prices)
- Money split: **equal thirds** within Index (~$3,333.33 per ETF before share rounding).
- **5-day history** section appears with multiple dates and dollar values per day.
- Trend line or text (UP / DOWN / FLAT) when at least 2 history points exist.

---

## Test Case 5 — Single strategy: Ethical Investing ($7,500)

**Goal:** Ethical strategy maps to assignment example stocks (plus extra tickers in our mapping).

**Steps:**

1. CLI: amount `7500`, strategy `ethical` or `1`  
   **OR** Web: `7500`, select **Ethical Investing** only.

**Expected results:**

- Holdings include **AAPL, ADBE, NSRGY** (and **MSFT** per our config — 4 stocks total).
- Four positions; allocation **~25% each** of $7,500 (~$1,875 per symbol).
- Composition grouped under **Ethical Investing**.
- Current prices are **non-zero** (live data); total portfolio value displayed.
- 5-day history table/chart populated (may be 3–5 trading days depending on market calendar).

---

## Test Case 6 — Two strategies: Growth + Value ($20,000)

**Goal:** User may pick **two** strategies; capital split **50% / 50%** between them.

**Steps:**

1. CLI: amount `20000`, strategies `growth, value` or `2, 5`  
   **OR** Web: `20000`, select **Growth** and **Value**, then generate.

**Expected results:**

- Growth tickers present: **TSLA, NVDA, AMD, NFLX, COIN** (5 stocks).
- Value tickers present: **BAC, F, XOM, JPM** (4 stocks).
- **9 total positions** (no duplicate tickers across strategies).
- Roughly **$10,000** notional per strategy group (equal split within each group among its stocks).
- Summary shows holdings **by strategy** (Growth block and Value block).
- Combined **Current Portfolio Value** and gain/loss vs $20,000 investment.

---

## Test Case 7 — Reject more than two strategies (CLI)

**Goal:** Enforce **1 or 2** strategies only.

**Steps:**

1. `python main.py`
2. Amount: `5000`
3. At strategy prompt enter: `1, 2, 3` (three selections)

**Expected results:**

- Message: enter **exactly 1 or 2** strategies; prompt repeats.
- Enter `1` only to finish test and exit if desired.

---

## Test Case 8 — Reject duplicate strategy (CLI)

**Goal:** Cannot select the same strategy twice.

**Steps:**

1. `python main.py`
2. Amount: `8000`
3. Enter: `ethical, ethical`

**Expected results:**

- Error: cannot select the **same strategy twice**.
- Prompt repeats until valid input.

---

## Test Case 9 — Invalid strategy name (CLI)

**Goal:** Invalid strategy names are rejected.

**Steps:**

1. `python main.py`
2. Amount: `6000`
3. Enter strategy: `crypto`

**Expected results:**

- Error indicating **invalid strategy** and listing valid options (`ethical`, `growth`, `index`, `quality`, `value`).
- No portfolio created until a valid strategy is entered.

---

## Test Case 10 — Web UI: chart, summary cards, and API error handling

**Goal:** Extra web features — visual 5-day trend, summary metrics, server-side validation.

**Part A — Successful run**

1. `python app.py` → `http://127.0.0.1:5001`
2. Amount: `15000`
3. Select **Quality Investing** only → **Generate Portfolio**

**Expected results (success):**

- Summary cards: **Total Investment**, **Current Value**, **Gain/Loss** (or return %).
- Holdings table with tickers **JNJ, KO, PG, UNH**.
- **5-day portfolio trend** chart (Chart.js) with dates on X-axis and portfolio value on Y-axis.
- Trend badge: **UP**, **DOWN**, or **FLAT** with change amount/percent.

**Part B — API validation (browser DevTools optional)**

1. With server still running, submit with **no strategy selected** and amount `15000`.

**Expected results (validation):**

- Client error: select **1 or 2** strategies (same as Test Case 3 pattern).

---

## Quick reference — requirement coverage

| Requirement | Covered by test(s) |
|-------------|-------------------|
| Min $5,000 input | 2, 3 |
| 1–2 strategies | 4–6, 7–8 |
| 5 strategies, ≥3 securities each | 1, 4–6 |
| Index / Ethical example mappings | 4, 5 |
| Stock selection output | 4–6, 10 |
| Money division | 4–6 |
| Live portfolio value | 4–6, 10 |
| 5-day weekly trend | 4–6, 10 |
| CLI + Web UI | 1–2, 7–9 CLI; 3–6, 10 Web |

---

## Notes for graders

- **Live data:** Prices and history depend on Yahoo Finance; values change by market hours. Tests check **structure and behavior**, not exact dollar amounts.
- **History length:** “5 days” uses the last **5 trading days** of market data; holidays may show fewer than 5 rows.
- **Port:** Web app uses **5001** (not 5000) to avoid macOS AirPlay conflicts.
- **Troubleshooting:** If `command not found: pip`, use `python3 -m pip` instead of `pip`. If `ModuleNotFoundError: yfinance`, run `python3 -m pip install -r requirements.txt` again inside your virtual environment.


