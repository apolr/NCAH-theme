# NCAH switch-over runbook (draft)

Nothing here touches the live site until you decide to run it. Aim: 30 to 45 minutes, with an undo path.

## Before the day (on staging if WHC.ca provides it)
1. Confirm a fresh JetBackup (done once on Nov 22, 2026; take another the day before).
2. Upload this theme (zip of the repo) and activate it on staging. Do not activate on live yet.
3. Pages to create or update from `content/*.html` (paste into the block editor code view, or use the seeding route): Welcome (front page), About us, Membership, Events, Contact Us, Programs, Donate, Privacy Policy.
4. Tools > NCAH migrate: dry run, then "Convert posts", then "Create starter programs".
5. MailPoet form "Stay in touch" (ID 1) was created on Nov 22, 2026 and is the footer signup by default.

## Findings from the live site (read only, Nov 22, 2026)
- Design direction (Nov 22, 2026): layout and simplicity modelled on ncabc.org: green top bar, header floating over a full-bleed hero, small uppercase menu, serif headings (Cormorant Garamond, a free stand-in for NCABC's Larken), Nunito Sans body (stand-in for Soleil), square red uppercase buttons, photo tile strip, green membership band with cards, one upcoming event card, simple dark footer.
- Fonts on the live site are Fira Sans (body, nav), Arsenal (section headings) and Roboto (buttons), so the theme now uses those. The GSI intro card heading on the live Welcome page uses Architects Daughter (one-off); not carried over unless you want it.
- WPForms 810 (Contact Us) notifies `{admin_email}`, not `info@ncahamilton.ca`. Change to info@ before launch.
- MailPoet license shows "expires in 7 days". The "Stay in touch" form (ID 1) now exists.
- SendWP is installed but disconnected. Test that contact and donation emails actually send.
- Donations now use the Zeffy plugin: the Donate page shows `[zeffy-donate]`, which uses the campaign set in Settings > Zeffy (currently the Green Spirit Initiative campaign). Confirm that is the right campaign for the main Donate page. Give stays active until Zeffy is confirmed, then can be retired.
- Keep Zeffy, Give (for now), WPForms Lite, MailPoet and SendWP active. Elementor, Elementor Pro and EMCP Lite stay until the quiet period ends.

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

## Staging findings (WHC Managed WordPress staging at /staging)
- Pages with embeds (Contact map, Membership Google Form) must be pasted or saved by a logged-in admin. Loading them from a Code Snippets run-once job strips the iframes.
- Run-once snippets execute before WordPress is fully loaded, so hook database and page work to wp_loaded.
- The migrate tool (Tools > NCAH migrate) now clears the Elementor template and builder flag on posts, so converted posts use the NCAH header and footer. Undo restores them.
- The logo file has an opaque grey background. It sits in a white box in the header. A transparent or white-background logo would look better.

## Gallery page
A new Gallery page (content/gallery.html, slug gallery) holds all seven videos. The Welcome page links to it from the Watch section. At switch-over: create the page, paste the content, and add Gallery to the menu if wanted.
