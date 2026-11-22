# NCAH switch-over runbook (draft)

Nothing here touches the live site until you decide to run it. Aim: 30 to 45 minutes, with an undo path.

## Before the day (on staging if WHC.ca provides it)
1. Confirm a fresh JetBackup (done once on Nov 22, 2026; take another the day before).
2. Upload this theme (zip of the repo) and activate it on staging. Do not activate on live yet.
3. Pages to create or update from `content/*.html` (paste into the block editor code view, or use the seeding route): Welcome (front page), About us, Membership, Events, Contact Us, Programs, Donate, Privacy Policy.
4. Tools > NCAH migrate: dry run, then "Convert posts", then "Create starter programs".
5. Save the MailPoet signup form ID (none exists yet; create one first) in the same screen.

## Findings from the live site (read only, Nov 22, 2026)
- WPForms 810 (Contact Us) notifies `{admin_email}`, not `info@ncahamilton.ca`. Change to info@ before launch.
- MailPoet has no forms yet; license shows "expires in 7 days".
- SendWP is installed but disconnected. Test that contact and donation emails actually send.
- Give has three forms (Soccer Donation, General Donations, Donation Form). Confirm id 2482 is the intended one.
- Keep Give, WPForms Lite, MailPoet and SendWP active. Elementor, Elementor Pro and EMCP Lite stay until the quiet period ends.

## Switch-over day
1. Appearance > Themes: activate NCAH (Astra stays installed as the undo path).
2. Settings > Reading: set the front page to Welcome. Set Menus: Welcome, About us, Membership, Events, Programs (Golden Eagles Hamilton), Contact Us.
3. Unpublish Programs (old) and Green Spirit Initiative pages if still empty; keep test, WooCommerce and Tickets pages.
4. Add 301 redirect `/golden-eagles-hamilton/` to `https://soccer.ncahamilton.ca/` (only once the Golden Eagles site is merged).
5. Purge LiteSpeed cache. Check every page on desktop and phone, then submit a test contact message and a test donation.

## Undo
Reactivate Astra (and keep Elementor active). Posts: Tools > NCAH migrate > Undo last conversion.

## After
Wait two to four quiet weeks, then deactivate and delete Elementor, Elementor Pro and EMCP Lite.
