import re, glob
U = {
 "Sweat-proof undershirts for office men": "No Indian brand found in a quick search. US brands such as Ejis are only available through import sites like Ubuy ([Ubuy](https://www.ubuy.co.in/product/2DG7F3P8-ejis-mens-sweat-proof-undershirt-v-neck-anti-odor-silver-micro-modal-sweat-pads)).",
 "Fan-cooled jackets for outdoor workers": "No consumer brand found. Generic fan jackets (about ₹2,300) and industrial cooling vests (Inuteq, Surakshit) are sold on IndiaMART ([IndiaMART](https://m.indiamart.com/impcat/cooling-vests.html)).",
 "Extra-large swim caps and chlorine wash for long hair": "Long-hair swim caps are already sold by Speedo, Airavat and Viva ([Kibi Sports](https://shop.kibisports.com/collections/vector-x/products/viva-swimming-silicone-stretchable-comfortable-swim-cap-for-long-hair-cover-tear-proof-design-head-cap)), but no one sells a cap-plus-hair-care kit made for long Indian hair.",
 "Makeup made for men": "1: Yaan Man, which calls itself India's first men's makeup brand and appeared on Shark Tank India ([NE Now](https://nenow.in/web-stories/who-is-the-founder-of-indias-first-mens-makeup-brand)).",
 "Back-hair shaver for men": "No Indian brand found. Only generic listings and imported brands such as BakBlade and Mangroomer ([IndiaMART](https://m.indiamart.com/impcat/mens-razors.html)).",
 "Recovery boxes for new mothers after birth": "1: Juno Mom sells a postpartum kit on Smytten ([Smytten](https://smytten.com/shop/product/gift-sets/natural-birth-postpartum-kit-hospital-bag-essential-for-new-moms/JMM0006AB1)).",
 "Forest bathing walks": "2–3: luxury resorts (Oberoi Sukhvilas, Pugdundee Safaris) offer it at their properties, and Bengaluru has seen one-off walks in Cubbon Park ([SheThePeople](https://www.shethepeople.tv/news/bangalore-forest-bathing-price-cubbon-park-4491970)). No regular city walks found.",
 "Walking football for people over 50": "No walking-football group found in a quick search.",
 "30-minute strength workouts for women over 40": "No dedicated Indian programme found in a quick search; general gyms and online coaches exist.",
 "Grooming visits at home for bedridden and elderly people": "No specialist found. Urban Company does general home haircuts ([Urban Company](https://www.urbancompany.com/delhi-ncr-mens-grooming-sector-63-gurgaon)), but not trained care for bedridden people.",
 "Small monthly support groups for new managers": "No paid peer group found. Only formal courses exist, such as IIM Indore's programme for first-time managers ([IIM Indore](https://iimidr.ac.in/mdp-calendar/leadership-development-program-for-first-time-managers/)).",
 "Bicycle on a monthly plan, repairs included": "1: Gro Club in Bengaluru rents bicycles to kids and adults with doorstep delivery and repairs ([Dealroom](https://app.dealroom.co/companies/gro_club)).",
 "Kids' bicycles on a monthly plan that grow with your child": "1: Gro Club in Bengaluru rents bicycles to kids and adults with doorstep delivery and repairs ([Dealroom](https://app.dealroom.co/companies/gro_club)).",
 "Regular shop-window cleaning for shops and clinics": "No dedicated shop-window service found; general cleaning companies do one-off jobs.",
 "Salon chairs for freelance beauticians, by the day": "No Indian chair-rental service found in a quick search.",
 "Handwritten thank-you cards for small businesses": "No Indian service found. US examples are Simply Noted and Handwrytten ([Simply Noted](https://simplynoted.com/collections/thank-you)).",
 "Checked drivers to take children to classes and activities": "No Indian app found. Informal school vans and private drivers are the substitute. The US model is HopSkipDrive ([TechCrunch](https://techcrunch.com/2016/01/26/hopskipdrive-the-ridesharing-startup-for-kids-grabs-10-2m-in-series-a-funding)).",
 "Fair sharing of parents' jewellery and keepsakes among siblings": "No friendly item-sharing service found. Lawyers and family mediators handle disputes after they start ([The Statesman](https://www.thestatesman.com/supplements/law/mediation-to-resolve-inheritance-1503327356.html)).",
 "Letters from Santa posted to children": "No Indian service found; overseas sellers on Etsy are the substitute.",
 "Paid visits to beautiful private gardens": "No one found. The UK's National Garden Scheme opens about 3,700 private gardens a year ([Country & Town House](https://www.countryandtownhouse.com/culture/the-national-open-garden-scheme-what-is-it)).",
 "Rent a guitar or keyboard, and the rent counts toward buying it": "2: Rentock (Mumbai) rents instruments online ([Gust](https://gust.com/companies/rentock)), and local shops such as OMR Musical (Chennai) rent and sell. No rent-to-own plan found.",
 "Video calls from Santa for your child": "No Indian live-Santa service found. Global apps like Portable North Pole are the substitute ([PNP](https://www.portablenorthpole.com/santa-village/blog/how-to-call-Santa-Claus)).",
 "Learn-to-ride bicycle camps for kids": "No one found in a quick search.",
 "Buy, sell and trade used sports gear": "1–2: Sports Galaxy (online trade-in store since 2019) ([Sports Galaxy](https://sportsgalaxy.in/?p=46335)), and general listings on OLX.",
 "A bicycle repair van that comes to your home or office": "1: Fix My Cycle (Chennai) books doorstep bicycle repairs in about 20 cities ([YourStory](https://yourstory.com/2020/01/chennai-startup-fix-my-cycle-doorstep-service)).",
 "Gift wish-lists for weddings, baby showers and housewarmings": "3: Wedding Wishlist (Chennai) ([Inc42](https://inc42.com/?p=162300)), ForMyShaadi and Kiki ([YourStory](https://yourstory.com/companies/kiki-wedding--baby-gift-registry)). At the limit; you would need a sharper angle, such as NRI guests.",
}
seen=set()
for f in sorted(glob.glob("batch_*.md")):
    txt=open(f,encoding="utf-8").read()
    parts=re.split(r"(?m)^(?=### )",txt)
    out=[]
    for p in parts:
        if p.startswith("### "):
            name=p.split("\n")[0][4:].strip()
            if name in U:
                p=re.sub(r"(\*\*Who does this in India now:\*\*).*", lambda m: m.group(1)+" "+U[name], p, count=1)
                seen.add(name)
        out.append(p)
    open(f,"w",encoding="utf-8").write("".join(out))
print("updated", len(seen), "missing:", set(U)-seen)
