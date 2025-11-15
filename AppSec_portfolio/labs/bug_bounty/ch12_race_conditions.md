# Chapter 12 – Race Conditions

## Mental Model

Two or more requests hit the same business operation at almost the same time →  
server state updates incorrectly because there is no proper locking.

You aren’t racing the OS; you’re racing the **business logic**:

- Balance checks vs debits
- Coupon usage vs redemption
- Role changes vs permission checks

## High-Value Targets

- Money / credit systems:
  - Wallet top-ups, withdrawals
  - Gift cards / promo codes
- Inventory:
  - Limited quantity items, reservations, tickets
- Account changes:
  - Email / phone changes with OTP
  - Role / plan upgrades or downgrades

## Recon Checklist

- Look for any “use once” or “limited” resources:
  - Coupons, discount codes, referral bonuses, free trials
- Read responses:
  - Messages like “You have X remaining,” “Can only be used once”
- Note endpoints that:
  - Change state (`POST /purchase`, `/redeem`, `/apply_coupon`)
  - Use IDs in body or query (`coupon_id`, `offer_id`)

## Practical Exploitation Strategy

1. **Capture a single legitimate request in Burp**
   - e.g., applying a coupon once.

2. **Send to Intruder or Turbo Intruder**
   - Position whole request as the payload.
   - Use attack type “Pitchfork” or “Sniper” with many concurrent threads.

3. **Fire 50–200 almost identical requests**
   - Sometimes you also fuzz a small value, like a random header, to dodge caching.

4. **Analyze responses**
   - Did the coupon get applied more than once?
   - Did your balance go negative?
   - Did you obtain multiple items instead of one?

## Signals of a Race Condition

- Some requests fail, some succeed, but **side effects** apply multiple times.
- Order of responses doesn’t match order of requests.
- Logs / UI show duplicated actions (“payment processed twice”).

## Automation Ideas

- Short Python script using `concurrent.futures` or `asyncio`:
  - Replays the same signed request N times.
- Use Burp Turbo Intruder templates for:
  - “Double spend”
  - “Use-after-free coupon”

## Reporting Tips

- Include:
  - Exact endpoint and body used
  - Number of concurrent requests needed to reproduce
  - Before / after balances, with screenshots
- Quantify impact:
  - “Allowed infinite use of one-time coupon”
  - “Could withdraw more than account balance”
- Suggest fixes:
  - Server-side locking / transactions
  - Idempotency keys for operations
  - Enforcing uniqueness at DB level (unique constraints)

## Common Mistakes

- Testing only once or twice instead of hammering enough requests
- Forgetting that most real races show up only in **state**, not in the raw response
- Not resetting state between tests (hard to reproduce if you burn the coupon)
