import pyperclip
import pyautogui
import time
import re
import platform # Para detectar el sistema operativo

# --- INPUT TEXT ---
# Pega aquí tu texto completo tal como lo proporcionaste
input_text = """
🌸 Chapter 3: The Cat and Mouse Game
Scene 3.1: Morning After Awkwardness (Implied)
Prompt: Interior, Han Areum's own apartment, early morning. Sunlight streams in. (Han Areum: Korean woman, late 20s/early 30s, analyst/designer, looking flustered and annoyed at herself, hair slightly disheveled. Wears a simple grey silk pajama set). She stares at her reflection in the bathroom mirror, replaying the previous night's events in her mind, a mix of regret and lingering excitement on her face.
Feeling: Flustered, Internal Conflict, Lingering Passion
Scene 3.2: Boardroom Power Play
Prompt: Interior, modern boardroom. (Han Areum: Korean woman, late 20s/early 30s, analyst/designer, exuding confidence in a striking red power dress that is impeccably tailored, delivering a presentation. She deliberately avoids eye contact with Junho). (Kang Junho: Korean man, early/mid 30s, CEO, watching her with a subtle, possessive smirk, outwardly calm but with an intense focus. Wears a sharp navy blue suit and a patterned silk tie).
Feeling: Confident Defiance, Possessive Gaze, Undercurrent of Tension
Scene 3.3: Hallway Whisper and Lingering Touch
Prompt: Interior, corporate hallway. (Kang Junho: Korean man, early/mid 30s, CEO, leans in close, his lips near Areum's ear, whispering provocatively. Wears navy blue suit). His fingers briefly, almost accidentally, brush her wrist as she passes. (Han Areum: Korean woman, late 20s/early 30s, analyst/designer, stops, a faint blush rising on her cheeks but her eyes flash with a challenge. Wears red power dress).
Feeling: Seductive Teasing, Electric Touch, Challenging Banter
Scene 3.4: Under-the-Table Encounter
Prompt: Interior, meeting room with international clients. Underneath a large conference table, close-up. (Kang Junho: Korean man, early/mid 30s, CEO, intentionally brushes his leg against Areum's, his hand briefly touching hers as they both reach for a dropped pen. His expression above the table remains professional). (Han Areum: Korean woman, late 20s/early 30s, analyst/designer, shoots him a sharp, warning glance from under the table, though her composure above is perfect. Their faces are momentarily very close).
Feeling: Secret Provocation, Hidden Tension, Risky Flirtation
Scene 3.5: The Rival Dinner Date
Prompt: Interior, upscale restaurant. (Han Areum: Korean woman, late 20s/early 30s, analyst/designer, smiling brightly and engagingly with Seo Minho (unseen or partially visible). Wears an elegant black lace top and a sleek skirt). She glances up, feigning surprise as (Kang Junho: Korean man, early/mid 30s, CEO, looking impeccably dressed in a dark tailored suit, enters the same restaurant with another attractive woman (Eunbi or a similar type, in a chic cocktail dress) on his arm).
Feeling: Calculated Coincidence, Jealous Maneuvering, Public Showdown
Scene 3.6: Areum's "Oppa" Counterattack at Dinner
Prompt: Interior, restaurant. (Han Areum: Korean woman, late 20s/early 30s, analyst/designer, approaches Junho's table holding a wine glass, her smile sweet but laced with venom. Wears black lace top). She addresses (Kang Junho: Korean man, early/mid 30s, CEO, who looks momentarily startled. Wears dark suit) as "Oppa" in front of his female companion (who looks annoyed and confused. Wears chic cocktail dress).
Feeling: Venomous Sweetness, Public Provocation, Turning the Tables
Scene 3.7: Office Confrontation - Desk Push
Prompt: Interior, Han Areum's office at night, dimly lit. (Kang Junho: Korean man, early/mid 30s, CEO, looking intense and slightly furious, has just pushed Areum (gently but firmly) against her desk. Wears dark suit, tie loosened). He stands very close, trapping her, their faces inches apart. (Han Areum: Korean woman, late 20s/early 30s, analyst/designer, looks back defiantly, a challenging glint in her eyes. Wears her office attire from the day, perhaps slightly disheveled).
Feeling: Intense Confrontation, Raw Emotion, Power Struggle
Scene 3.8: The Accidental Call and Shared Dreams
Prompt: Split screen. Left: (Han Areum: Korean woman, late 20s/early 30s, analyst/designer, in her bed, looking frustrated and restless, accidentally dials Junho. Wears simple silk pajamas). Right: (Kang Junho: Korean man, early/mid 30s, CEO, in his penthouse bed, answers his phone, voice sleepy but a knowing smile forms as he realizes it's her. Wears pajama bottoms, possibly shirtless). He teases her about dreaming of him.
Feeling: Accidental Intimacy, Shared Longing, Playful Teasing
🌸 Chapter 4: We're Not the Same... But Not So Different Either
Scene 4.1: Return to the Old Street Food Stall
Prompt: Exterior, bustling street food stall area at night, colorful lights. (Kang Junho: Korean man, early/mid 30s, CEO, smiling genuinely, looking more relaxed than usual. Wears a casual dark grey knit sweater and dark jeans). He gestures towards their old favorite tteokbokki stall. (Han Areum: Korean woman, late 20s/early 30s, analyst/designer, looking at the stall with a nostalgic, surprised expression. Wears a comfortable beige trench coat over a simple blouse and jeans).
Feeling: Nostalgia, Relaxed Atmosphere, Shared Past
Scene 4.2: Soju and Jealous Confessions
Prompt: Exterior, sitting at a small table at the street food stall. Bottles of soju and plates of food between them. (Kang Junho: Korean man, early/mid 30s, CEO, looking directly at Areum with serious, honest eyes as he confesses his jealousy. Wears dark grey knit sweater). (Han Areum: Korean woman, late 20s/early 30s, analyst/designer, pauses mid-drink, looking surprised and then amused by his confession. Wears beige trench coat).
Feeling: Honest Confession, Surprised Amusement, Vulnerability
Scene 4.3: The "Resign for Me" Offer
Prompt: Exterior, street food stall. (Kang Junho: Korean man, early/mid 30s, CEO, earnest and serious as he suggests Areum resign so their work doesn't interfere. Wears dark grey knit sweater). (Han Areum: Korean woman, late 20s/early 30s, analyst/designer, eyes wide with disbelief, then bursting into laughter, finding his K-drama cliché offer both ridiculous and endearing. Wears beige trench coat).
Feeling: Grand Gesture, Disbelieving Laughter, Endearing Cliché
Scene 4.4: Laughter Like Old Times
Prompt: Exterior, street food stall. (Kang Junho: Korean man, early/mid 30s, CEO) and (Han Areum: Korean woman, late 20s/early 30s, analyst/designer) are both laughing heartily, heads thrown back, thoroughly enjoying the moment and each other's company. They wear their casual evening outfits (Junho: dark grey sweater, Areum: beige trench). The atmosphere is light and joyful, reminiscent of their past happiness.
Feeling: Unrestrained Joy, Rekindled Connection, Nostalgic Happiness
Scene 4.5: Walking by the Han River - First Kiss Memory
Prompt: Exterior, walking along the path by the Han River at night. The Banpo Bridge with its rainbow lights is visible in the background. (Han Areum: Korean woman, late 20s/early 30s, analyst/designer, stops and looks towards the bridge with a soft, reminiscent smile. Wears beige trench coat). She quietly mentions it was the site of their first kiss. (Kang Junho: Korean man, early/mid 30s, CEO, stops beside her, his expression also softening with the memory. Wears dark grey sweater).
Feeling: Shared Memory, Nostalgic Romance, Lingering Feelings
Scene 4.6: A Moment of Unspoken Tension
Prompt: Exterior, under the Banpo Bridge. (Han Areum: Korean woman, late 20s/early 30s, analyst/designer) and (Kang Junho: Korean man, early/mid 30s, CEO) stand close, their gazes locked. The vibrant lights of the bridge reflect in their eyes. There's a palpable tension, an unspoken question of "what now?" between them. No kiss, just intense eye contact. They wear their casual evening outfits.
Feeling: Intense Eye Contact, Unspoken Question, Electric Tension
Scene 4.7: Vulnerable Honesty on a Park Bench
Prompt: Exterior, park bench overlooking the Han River at night. (Kang Junho: Korean man, early/mid 30s, CEO, looking vulnerable and sad as he admits his loneliness since she left. Wears dark grey sweater). (Han Areum: Korean woman, late 20s/early 30s, analyst/designer, listens with a conflicted but empathetic expression, her hands clasped in her lap. Wears beige trench coat).
Feeling: Vulnerable Admission, Empathetic Conflict, Deep Sadness
Scene 4.8: The Drive Home - A Silent Understanding
Prompt: Interior, Junho's luxury car, night. Soft instrumental music plays. (Han Areum: Korean woman, late 20s/early 30s, analyst/designer, leans her head against the window, looking out at the city lights, a thoughtful expression on her face. Wears beige trench coat). (Kang Junho: Korean man, early/mid 30s, CEO, drives, occasionally glancing at her with a mix of hope and patience. Wears dark grey sweater). A comfortable, meaningful silence fills the car.
Feeling: Thoughtful Silence, Hopeful Patience, Unspoken Understanding
🌸 Chapter 5: Are We Dating… Or Falling in Love Again?
Scene 5.1: Playful Dates and Hidden Feelings
Prompt: Exterior, a beautiful garden full of wildflowers, sunny day. (Han Areum: Korean woman, late 20s/early 30s, analyst/designer, laughing as she runs playfully ahead. Wears a light blue floral print sundress and white sneakers). (Kang Junho: Korean man, early/mid 30s, CEO, chasing after her with a wide, happy smile, looking carefree. Wears a casual white linen shirt and beige chinos).
Feeling: Joyful Carefreeness, Playful Romance, Rekindled Happiness
Scene 5.2: Captured in a Photograph
Prompt: Exterior, cherry blossom park. (Han Areum: Korean woman, late 20s/early 30s, analyst/designer, looks down at her camera screen, a soft, surprised blush on her cheeks. Wears a cream-colored knit cardigan over a simple top and jeans). The camera display shows a photo she just took of (Kang Junho: Korean man, early/mid 30s, CEO, who stands a short distance away under a cherry tree, gazing at her with undisguised adoration, unaware he was photographed. Wears a light blue casual button-down shirt).
Feeling: Captured Adoration, Surprised Blush, Undeniable Love
Scene 5.3: The Ice Cream Tease
Prompt: Exterior, park bench. Close-up. (Han Areum: Korean woman, late 20s/early 30s, analyst/designer, playfully wipes a drip of melted ice cream from Jin-sun's hand with a napkin. Wears cream cardigan). Their faces are very close, lips almost touching, a charged silence between them. (Kang Junho: Korean man, early/mid 30s, CEO, looks at her intensely, his voice a low murmur as he questions her teasing. Wears light blue shirt).
Feeling: Teasing Proximity, Charged Silence, Unspoken Desire
Scene 5.4: The "What Are We?" Moment
Prompt: Exterior, park path on an overcast day, fingers intertwined. (Han Areum: Korean woman, late 20s/early 30s, analyst/designer, stops walking, looking up at Junho with an adorable pout and questioning eyes. Wears a stylish grey trench coat). (Kang Junho: Korean man, early/mid 30s, CEO, stops and looks down at her with a knowing, gentle smile. Wears a dark navy peacoat).
Feeling: Adorable Pout, Questioning Gaze, Defining the Relationship
Scene 5.5: The Boutique Proposition
Prompt: Exterior, park. (Kang Junho: Korean man, early/mid 30s, CEO, looking serious but with a loving smile, proposes the boutique idea. Wears navy peacoat). (Han Areum: Korean woman, late 20s/early 30s, analyst/designer, initially looks thoughtful, then a wide, mischievous, and dreamy smile spreads across her face as she names her desire. Wears grey trench coat).
Feeling: Grand Offer, Dreamy Aspiration, Playful Negotiation
Scene 5.6: The "Be My Girlfriend" Kiss
Prompt: Exterior, park. (Han Areum: Korean woman, late 20s/early 30s, analyst/designer, covers her face with her hands, laughing and overwhelmed with emotion after accepting his proposal to be his girlfriend. Wears grey trench coat). (Kang Junho: Korean man, early/mid 30s, CEO, gently pulls her hands away and cups her face, kissing her deeply and passionately. Wears navy peacoat). The kiss is full of joy, promise, and renewed commitment.
Feeling: Overwhelming Joy, Passionate Commitment, New Beginning
Scene 5.7: Resignation and a Private Embrace
Prompt: Interior, a modern meeting room, moments after Areum resigns. The door is closed. (Kang Junho: Korean man, early/mid 30s, CEO, professional facade dropped, pulls Areum into a tight embrace from behind, nuzzling her neck. Wears a charcoal grey suit). (Han Areum: Korean woman, late 20s/early 30s, analyst/designer, leans back into him, smiling, a sense of freedom and excitement in her eyes. Wears a smart black dress suitable for her last day).
Feeling: Private Celebration, Freedom, Loving Embrace
Scene 5.8: Dreams Taking Shape - Boutique Visit
Prompt: Exterior, in front of an empty shopfront with large windows, future site of Areum's boutique. (Kang Junho: Korean man, early/mid 30s, CEO, playfully lifts Areum in his arms, both laughing. Wears a stylish casual blazer and dark jeans). (Han Areum: Korean woman, late 20s/early 30s, analyst/designer, wraps her arms around his neck, looking ecstatic and full of dreams. Wears a chic olive green jumpsuit). They share a joyful, public kiss.
Feeling: Shared Dreams, Joyful Exuberance, Public Display of Affection
🌸 Chapter 6: The Boutique, The Ex, and The Fire of Love
Scene 6.1: Boutique Grand Opening - Areum Shines
Prompt: Interior, Han Areum Exclusive boutique grand opening. Elegant decor, white petals. (Han Areum: Korean woman, late 20s/early 30s, designer, looking radiant and confident, addressing fashion press and guests. Wears a stunning self-designed cream-colored sheath dress that is both elegant and modern). (Kang Junho: Korean man, early/mid 30s, CEO, stands slightly to the side, beaming with pride, impeccably dressed in a black tailored suit and a grey silk tie).
Feeling: Radiant Confidence, Proud Support, Successful Launch
Scene 6.2: The Venomous Ex Arrives
Prompt: Interior, boutique opening. (Eunbi: Korean woman, late 20s/early 30s, striking in a bold red cocktail dress that contrasts with the white decor, red lips curved in a venomous smile). She approaches (Kang Junho: Korean man, early/mid 30s, CEO, whose expression becomes tense. Wears black suit). Areum observes them from a distance, her intuition on high alert.
Feeling: Unwelcome Intrusion, Venomous Presence, Rising Tension
Scene 6.3: Areum's Calm Confrontation
Prompt: Interior, boutique opening. (Han Areum: Korean woman, late 20s/early 30s, designer, stands confidently between Eunbi and Junho, her gaze direct and unwavering. Wears cream dress). She calmly but firmly addresses (Eunbi: Korean woman, late 20s/early 30s, who looks momentarily taken aback by Areum's composure. Wears red dress). Junho watches, a mix of concern and admiration on his face.
Feeling: Calm Strength, Dignified Confrontation, Protective Stance
Scene 6.4: Eunbi's Failed Parting Shot
Prompt: Interior, boutique opening. (Eunbi: Korean woman, late 20s/early 30s, attempts a final, cutting remark, her smile forced. Wears red dress). (Han Areum: Korean woman, late 20s/early 30s, designer, maintains her graceful smile, delivering a poised and confident comeback that silences Eunbi. Wears cream dress). Eunbi turns and leaves, clearly defeated.
Feeling: Grace Under Pressure, Confident Retort, Moral Victory
Scene 6.5: Junho's Overwhelming Pride
Prompt: Interior, boutique opening, a quiet corner behind a clothing rack or display. (Kang Junho: Korean man, early/mid 30s, CEO, pulls Areum close, his eyes shining with immense pride and love. Wears black suit). He whispers his admiration to (Han Areum: Korean woman, late 20s/early 30s, designer, who looks up at him, a mixture of relief and happiness on her face. Wears cream dress).
Feeling: Immense Pride, Deep Love, Shared Triumph
Scene 6.6: The Victory Kiss
Prompt: Interior, hidden corner of the boutique. (Kang Junho: Korean man, early/mid 30s, CEO, cups Areum's face gently. Wears black suit). He kisses (Han Areum: Korean woman, late 20s/early 30s, designer, who melts into the kiss, all tension gone. Wears cream dress). The kiss is slow, deep, filled with respect, desire, and shared victory.
Feeling: Respectful Desire, Shared Victory, Deepening Love
Scene 6.7: Celebrating Success and New Beginnings
Prompt: Interior, Junho's penthouse, night. Soft lighting. (Han Areum: Korean woman, late 20s/early 30s, designer, shoes kicked off, relaxing on the sofa with a glass of wine, a contented smile on her face. Wears her cream dress, perhaps slightly unzipped at the back). (Kang Junho: Korean man, early/mid 30s, CEO, sits beside her, tie loosened, arm around her, also holding a wine glass. Wears black suit trousers and white shirt). They toast to their future.
Feeling: Contented Relaxation, Shared Success, Intimate Celebration
Scene 6.8: Ready for Everything, Together
Prompt: Interior, Junho's penthouse. (Han Areum: Korean woman, late 20s/early 30s, designer, looks at Junho with tender, determined eyes. Wears cream dress). Says she's ready for everything with him. (Kang Junho: Korean man, early/mid 30s, CEO, gazes back at her with deep love and reassurance. Wears white shirt, suit jacket off). They lean in for another heartfelt kiss, sealing their commitment.
Feeling: Tender Commitment, Mutual Reassurance, Unstoppable Love
🌸 Chapter 7: The Place Where It All Began
Scene 7.1: Junho's Quiet Admiration at the Boutique
Prompt: Interior, Han Areum Exclusive boutique, daytime. Bright and chic. (Han Areum: Korean woman, late 20s/early 30s, designer, focused on arranging dresses on a rack, looking professional and passionate. Wears an elegant navy blue A-line dress of her own design). (Kang Junho: Korean man, early/mid 30s, CEO, sits comfortably on a plush armchair in the boutique, watching her work with a soft, admiring gaze. Wears a smart casual outfit: a light grey cashmere sweater and dark chinos).
Feeling: Quiet Admiration, Supportive Presence, Pride
Scene 7.2: The Painful "Why We Broke Up" Conversation
Prompt: Interior, boutique. (Han Areum: Korean woman, late 20s/early 30s, designer, turns to Junho, her expression serious but gentle as she explains the real reason for their past breakup. Wears navy A-line dress). (Kang Junho: Korean man, early/mid 30s, CEO, expression shifts from admiration to shock, then dawning guilt and pain as he listens. Wears light grey cashmere sweater). The atmosphere becomes heavy with unspoken regret.
Feeling: Painful Revelation, Guilt, Understanding Past Hurt
Scene 7.3: Junho's Silent Torment
Prompt: Interior, Junho's penthouse office, late at night. Dimly lit, only a desk lamp on. (Kang Junho: Korean man, early/mid 30s, CEO, looking tormented and sleepless, tie undone, shirt sleeves rolled up. Wears his office attire from earlier but disheveled). He stares blankly at his computer screen, clearly unable to focus, replaying Areum's words.
Feeling: Guilt, Regret, Sleepless Torment
Scene 7.4: The Mysterious Summons
Prompt: Exterior, street outside Areum's boutique, late afternoon, five days later. (Kang Junho: Korean man, early/mid 30s, CEO, looking composed but with an underlying intensity, stands beside his black luxury sedan. Wears a crisp white shirt and a stylish grey sports jacket). He looks directly at (Han Areum: Korean woman, late 20s/early 30s, designer, who approaches him with a mixture of annoyance and curiosity. Wears a chic olive green blouse and black tailored trousers).
Feeling: Mysterious Intent, Tense Curiosity, Anticipation
Scene 7.5: Return to the University Campus
Prompt: Exterior, university campus grounds, familiar buildings in the background. Late afternoon light. (Han Areum: Korean woman, late 20s/early 30s, designer, looking around with a nostalgic, slightly emotional expression. Wears olive green blouse and black trousers). Walks beside (Kang Junho: Korean man, early/mid 30s, CEO, guiding her gently, his face unreadable but purposeful. Wears white shirt, grey sports jacket).
Feeling: Nostalgia, Emotional Resonance, Purposeful Journey
Scene 7.6: The Auditorium - Reliving a First Spark
Prompt: Interior, empty university auditorium, stage dimly lit. (Kang Junho: Korean man, early/mid 30s, CEO, smiling softly as he recounts seeing Areum in her first student fashion show. Wears white shirt, grey sports jacket). (Han Areum: Korean woman, late 20s/early 30s, designer, also smiling, remembering the moment and his handmade paper flower. Wears olive green blouse). The atmosphere is filled with bittersweet memories.
Feeling: Bittersweet Memories, Shared History, Gentle Reminiscence
Scene 7.7: The Proposal
Prompt: Interior, university auditorium stage. (Kang Junho: Korean man, early/mid 30s, CEO, kneeling on one knee, holding open a small velvet ring box revealing a delicate diamond flower ring. His eyes are filled with sincere love and hopeful vulnerability. Wears white shirt, grey sports jacket). He proposes to (Han Areum: Korean woman, late 20s/early 30s, designer, hands covering her mouth, tears of joy and shock streaming down her face. Wears olive green blouse).
Feeling: Overwhelming Joy, Sincere Proposal, Hopeful Vulnerability
Scene 7.8: An Emphatic "Yes!" and a Kiss of Reunion
Prompt: Interior, university auditorium stage. (Han Areum: Korean woman, late 20s/early 30s, designer, throws her arms around Junho's neck, crying and laughing as she says "Yes!". Wears olive green blouse). (Kang Junho: Korean man, early/mid 30s, CEO, still kneeling or rising, embraces her tightly, his face buried in her neck, immense relief and happiness washing over him. Wears white shirt, grey sports jacket). They then pull back slightly to share a deeply emotional, tear-filled kiss.
Feeling: Ecstatic Acceptance, Profound Relief, Emotional Reunion Kiss
🌸 Chapter 8: Between Dresses and Promises
Scene 8.1: Wedding Planning Nights
Prompt: Interior, cozy living room of their home, late evening. Scattered wedding planning materials (guest lists, fabric swatches) on a coffee table. (Han Areum: Korean woman, late 20s/early 30s, designer, looking slightly stressed but happy, pointing at a list. Wears comfortable loungewear: a soft pink cashmere sweater and grey leggings). Discusses guest list with (Kang Junho: Korean man, early/mid 30s, CEO, looking amused and affectionate, also in comfortable attire: a dark blue t-shirt and lounge pants).
Feeling: Happy Stress, Domestic Intimacy, Shared Planning
Scene 8.2: Secret Visit to the Second Boutique
Prompt: Interior, chic new boutique in Itaewon, grand opening day. Bright and airy. (Han Areum: Korean woman, late 20s/early 30s, designer, looks professional and radiant, overseeing the event. Wears an elegant beige pantsuit). She catches a glimpse in a mirror reflection of (Kang Junho: Korean man, early/mid 30s, CEO, trying to be incognito with dark sunglasses and a baseball cap, leaving a single flower and a note. Wears a casual dark jacket). She smiles knowingly.
Feeling: Secret Support, Playful Gesture, Knowing Smile
Scene 8.3: Playful Seduction After a Long Day
Prompt: Interior, their home, living room. (Han Areum: Korean woman, late 20s/early 30s, designer, with a mischievous smile, playfully pushes Junho onto the sofa. Wears a stylish silk blouse and skirt, her "work" attire). She sits astride him, slowly unbuttoning his shirt. (Kang Junho: Korean man, early/mid 30s, CEO, looks up at her with desire and amusement, surrendering to her advances. Wears a dress shirt and trousers, tie loosened).
Feeling: Playful Seduction, Desirous Amusement, Reconnecting Passion
Scene 8.4: The Perfect Wedding Dress Moment
Prompt: Interior, elegant bridal atelier. (Han Areum: Korean woman, late 20s/early 30s, designer, stands in front of a large mirror, wearing her stunning white wedding dress with a striking red bow detail at the waist. Her expression is one of quiet awe and happiness). The designer (unseen or blurred) makes a final adjustment.
Feeling: Breathtaking Beauty, Dream Realized, Quiet Awe
Scene 8.5: Whispers of a Honeymoon
Prompt: Interior, their bedroom, late night, wrapped in sheets. Soft moonlight. (Han Areum: Korean woman, late 20s/early 30s, designer, snuggled against Junho, whispering about honeymoon plans. Wears a simple silk nightgown). (Kang Junho: Korean man, early/mid 30s, CEO, holding her close, stroking her back, a tender smile on his face as he suggests Paris. Wears pajama bottoms).
Feeling: Intimate Whispers, Romantic Planning, Tender Affection
Scene 8.6: Dinner with Future In-Laws
Prompt: Interior, elegant dining room at Junho's family home. (Junho's Mother: Gracious older Korean woman, warmly holding Areum's hand across the dinner table, expressing her happiness. Wears a traditional hanbok or elegant dress). (Han Areum: Korean woman, late 20s/early 30s, designer, smiling sincerely, feeling welcomed. Wears a sophisticated dark green dress). (Kang Junho: Korean man, early/mid 30s, CEO, watches them from the head of the table with pride and love. Wears a smart blazer and shirt).
Feeling: Family Acceptance, Warm Welcome, Shared Happiness
Scene 8.7: Eve of the Wedding Messages
Prompt: Split screen or quick cuts. Left: (Han Areum: Korean woman, late 20s/early 30s, designer, in her childhood bedroom or a hotel room, smiling as she types on her phone. Wears comfortable pajamas). Right: (Kang Junho: Korean man, early/mid 30s, CEO, in his own room, also on his phone, a mix of nerves and excitement on his face. Wears a t-shirt and pajama pants). They exchange loving and teasing messages late into the night.
Feeling: Anticipation, Loving Exchange, Pre-Wedding Jitters
Scene 8.8: Building a "We"
Prompt: Montage of small, intimate moments: Junho leaving a flower on Areum's design table; Areum surprising Junho with his favorite coffee at his office; them laughing while trying to assemble a piece of furniture; a quiet embrace on their balcony overlooking the city. The overall mood is one of deep connection and joyful partnership as they build their life together leading up to the wedding.
Feeling: Joyful Partnership, Deep Connection, Building a Future
🌸 Chapter 9: Yes, Forever
Scene 9.1: Areum's Wedding Day Radiance
Prompt: Interior, bridal suite, bright morning light. (Han Areum: Korean woman, late 20s/early 30s, bride, looking stunning, makeup being finalized. Her dark brown hair is elegantly styled. She wears a white silk robe). She gazes at her reflection with a calm, radiant smile, a sense of peace and excitement in her eyes.
Feeling: Radiant Joy, Calm Excitement, Bridal Beauty
Scene 9.2: Junho's Pre-Wedding Nerves
Prompt: Interior, groom's dressing room at the wedding venue. (Kang Junho: Korean man, early/mid 30s, groom, looking incredibly handsome in his perfectly tailored black tuxedo and white bow tie, but repeatedly adjusting his bow tie, a nervous yet hopeful expression on his face). His best friend (similar age, also in a tux) tries to calm him down with a reassuring smile.
Feeling: Nervous Anticipation, Hopeful Excitement, Groom's Jitters
Scene 9.3: The Bride's Entrance
Prompt: Interior, beautifully decorated wedding hall, aisle lined with white flowers. All guests stand. (Han Areum: Korean woman, late 20s/early 30s, bride, walking down the aisle, looking breathtaking in her classic white wedding dress with the striking red bow at the waist. Her eyes are fixed on Junho, a loving smile on her face). The focus is on her radiant beauty and the emotional impact of her entrance.
Feeling: Breathtaking Entrance, Emotional Climax, Pure Love
Scene 9.4: Junho's Awestruck Gaze
Prompt: Interior, wedding hall, at the altar. Close-up on (Kang Junho: Korean man, early/mid 30s, groom, completely awestruck, tears welling in his eyes as he watches Areum approach. Wears black tuxedo). His breath catches, and he whispers how beautiful she is.
Feeling: Awestruck Love, Overwhelming Emotion, Pure Adoration
Scene 9.5: Exchanging Vows and Rings
Prompt: Interior, wedding altar, soft lighting. (Han Areum: Korean woman, late 20s/early 30s, bride) and (Kang Junho: Korean man, early/mid 30s, groom) face each other, hands clasped, eyes locked. They exchange heartfelt, tearful vows. Close-up on their hands as they exchange simple, elegant wedding bands.
Feeling: Heartfelt Vows, Tearful Commitment, Eternal Promise
Scene 9.6: The First Kiss as Husband and Wife
Prompt: Interior, wedding altar. (Kang Junho: Korean man, early/mid 30s, groom, gently lifts Areum's veil (if she has one) or cups her face. Wears black tuxedo). He kisses (Han Areum: Korean woman, late 20s/early 30s, bride, smiling through happy tears. Wears wedding dress) with profound love and tenderness, a kiss that feels like the first true kiss of their lives together. Guests applaud joyfully in the background.
Feeling: Profound Love, Tender First Kiss, Joyful Celebration
Scene 9.7: The First Dance
Prompt: Interior, wedding reception, dance floor under warm, romantic lighting. (Han Areum: Korean woman, late 20s/early 30s, bride, dancing closely with Junho, her head resting on his shoulder. Wears wedding dress). (Kang Junho: Korean man, early/mid 30s, groom, holds her tightly, a look of deep contentment on his face. Wears black tuxedo). They sway slowly, lost in their own world.
Feeling: Romantic Intimacy, Contented Love, Shared Bliss
Scene 9.8: Honeymoon Suite Seduction
Prompt: Interior, luxurious hotel suite in Seoul, night. Petals scattered, soft candlelight. (Han Areum: Korean woman, late 20s/early 30s, new wife, wearing a delicate white silk bridal robe, hair loose, approaches Junho with a sweet, slightly nervous but happy expression. Wears bridal robe). (Kang Junho: Korean man, early/mid 30s, new husband, looks at her with adoration and desire, gently drawing her into an embrace. Wears a silk dressing gown or shirt and trousers).
Feeling: Bridal Seduction, Adoring Desire, Intimate Happiness
🌸 Chapter 10: Even if Fate Changes, I Choose You
Scene 10.1: The Reality of Married Life & Work
Prompt: Montage: Areum looking stressed but determined in her bustling Itaewon boutique, sketching designs late at night. Junho arriving home late from HanKang Group, looking tired but bringing takeout for Areum. Them sharing a quick, tired kiss before collapsing into their separate work modes.
Feeling: Hectic Reality, Enduring Support, Married Life Challenges
Scene 10.2: The "Baby Talk" and Silent Fear
Prompt: Interior, their home dining area, after a quiet dinner. (Han Areum: Korean woman, late 20s/early 30s, wife/designer, looks thoughtfully at Junho, asking about having a baby. Wears comfortable but chic loungewear: a soft grey cashmere cardigan and silk trousers). (Kang Junho: Korean man, early/mid 30s, husband/CEO, expression becomes guarded, a flicker of fear in his eyes. Wears a dark blue knit polo shirt and dark trousers).
Feeling: Hopeful Question, Hidden Fear, Unspoken Worries
Scene 10.3: The Doctor's Office - Difficult News
Prompt: Interior, doctor's consultation room. (Han Areum: Korean woman, late 20s/early 30s, wife/designer, listens to the doctor (unseen) with a brave face, then reaches out to tightly grip Junho's hand. Wears an elegant beige blouse and black skirt). (Kang Junho: Korean man, early/mid 30s, husband/CEO, looking down, devastated and unable to meet Areum's eyes. Wears a light grey suit, tie loosened).
Feeling: Devastating News, Shared Grief, Unwavering Support
Scene 10.4: Junho's Vulnerability and Areum's Strength
Prompt: Interior, their bedroom, night. (Kang Junho: Korean man, early/mid 30s, husband/CEO, finally breaks down, confessing his feelings of failure, crying into Areum's shoulder. Wears simple t-shirt and pajama pants). (Han Areum: Korean woman, late 20s/early 30s, wife/designer, holds him tightly, her expression strong and loving, reassuring him. Wears a soft silk pajama set).
Feeling: Vulnerable Breakdown, Loving Reassurance, Unconditional Love
Scene 10.5: A New Adventure - Redefining Family
Prompt: Exterior, Han River park, sunny day. (Han Areum: Korean woman, late 20s/early 30s, wife/designer, looking vibrant and hopeful, suggests traveling and new adventures. Wears a stylish bright yellow trench coat and jeans). (Kang Junho: Korean man, early/mid 30s, husband/CEO, looks at her with renewed love and admiration, a genuine smile returning to his face. Wears a casual navy blue jacket and chinos).
Feeling: Hopeful Proposition, Renewed Spirit, Redefining Happiness
Scene 10.6: Reconnecting Through Small Gestures
Prompt: Montage: Junho surprising Areum with flowers at her boutique. Areum leaving a cute sticky note on Junho's laptop ("I love you even when you snore!"). Them cooking together on a weekend, laughing over a minor kitchen mishap. A close-up of their hands intertwined as they talk before bed.
Feeling: Rekindled Intimacy, Loving Gestures, Rebuilding Connection
Scene 10.7: Areum's "Real Women" Collection
Prompt: Interior, Areum's boutique or design studio. (Han Areum: Korean woman, late 20s/early 30s, wife/designer, looking passionate and inspired as she sketches designs for her new clothing line for "real women". Wears a chic, comfortable design of her own, perhaps a flowing blouse and wide-leg trousers). (Kang Junho: Korean man, early/mid 30s, husband/CEO, watches her with pride and full support, perhaps reviewing her business plan with a nod. Wears a smart casual blazer).
Feeling: Inspired Creation, Unwavering Support, Meaningful Legacy
Scene 10.8: The Essential Love
Prompt: Interior, their home, living room, softly lit. Jazz music playing. (Han Areum: Korean woman, late 20s/early 30s, wife/designer, looks at Junho with deep, content love, reassuring him that their family is complete. Wears an elegant silk loungewear set). (Kang Junho: Korean man, early/mid 30s, husband/CEO, gazes back at her, his eyes filled with profound gratitude and love, understanding dawning. Wears a comfortable dark sweater). He leans in to kiss her, a kiss of complete acceptance and essential love.
Feeling: Profound Acceptance, Essential Love, Complete Family
"""

# --- PROCESAMIENTO DEL TEXTO ---
prompts_to_paste = []
print("--- INICIO DEBUG ---")
# Usamos una expresión regular para encontrar el texto entre "Prompt:" y "Feeling:"
matches = re.findall(r'Prompt:(.*?)Feeling:', input_text, re.DOTALL | re.IGNORECASE)

# Imprimimos cuántos encontró DIRECTAMENTE la función re.findall
print(f"Número de matches encontrados por re.findall: {len(matches)}")

for match in matches:
    # Limpiamos espacios/saltos de línea al inicio y final de cada prompt
    clean_prompt = match.strip()
    if clean_prompt: # Nos aseguramos de que no esté vacío
        prompts_to_paste.append(clean_prompt)

# --- AUTOMATIZACIÓN ---
print(f"Encontrados {len(prompts_to_paste)} prompts para pegar.") # Informa cuántos va a pegar
print("Preparado para pegar los prompts.")
print("Tienes 5 segundos para cambiar a la ventana de la aplicación donde quieres pegar...")

# Espera 5 segundos para que cambies de ventana
time.sleep(10)

# Determinar la tecla de comando/control según el SO
paste_key = 'ctrl' if platform.system() == 'Windows' else 'command' # 'command' para macOS

print("Comenzando a pegar...")

total_prompts = len(prompts_to_paste) # Guardamos el total para la comprobación final

for i, prompt in enumerate(prompts_to_paste):
    # 'i' empieza en 0, así que el número de prompt actual es i + 1
    current_prompt_number = i + 1
    print(f"Pegando prompt {current_prompt_number}/{total_prompts}...")

    # 1. Copiar el texto al portapapeles
    pyperclip.copy(prompt)
    time.sleep(0.2) # Pequeña pausa para asegurar que se copió

    # 2. Pegar (Simular Ctrl+V o Cmd+V)
    pyautogui.hotkey(paste_key, 'v')
    time.sleep(0.2) # Pequeña pausa después de pegar

    # 3. Presionar Enter
    pyautogui.press('enter')

    # 4. Esperar 1 segundo estándar después de cada prompt
    print("Esperando 1 segundo...")
    time.sleep(1)

    # --- NUEVA LÓGICA DE PAUSA ADICIONAL ---
    # 5. Comprobar si el número de prompt actual es múltiplo de 10
    #    Y asegurarse de que no sea el último prompt (para no esperar innecesariamente al final)
    if current_prompt_number % 10 == 0 and current_prompt_number < total_prompts:
        print(f"--- Fin del ciclo {current_prompt_number}. Pausa adicional de 30 segundos... ---")
        time.sleep(30)
        print("--- Pausa adicional terminada. Continuando... ---")
    # --- FIN DE LA NUEVA LÓGICA ---

print(f"¡Proceso completado! Se pegaron {total_prompts} prompts.")