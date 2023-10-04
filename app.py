import openai
import random
import gradio as gr
import os


openai.api_key = os.environ["OpenAPI_Key"]

manual = r"""Deze tool werkt met 2 soorten input:

1.   Een leerdoel, zoals:

Het rechterventrikel wordt van bloed voorzien door de rechter coronairarterie (RCA).

2.    De complete HTML-code van een opgave in de MES Editor, zoals:

Exercise body:

<mc:exercise xmlns:mc="http://www.expertcollege.com/mes/multiple-choice/exercise"><mc:question><![CDATA[Theorie:<br />Het rechterventrikel wordt van bloed voorzien door de rechter coronairarterie (RCA). Direct na het ontspringen uit de sinus aortae geeft de RCA twee takken af.<br /><br />Stelling:<br />Dit zijn onder andere de .....]]></mc:question><mc:choices><mc:choice id="1"><![CDATA[Ramus descendens posterior]]></mc:choice><mc:choice id="2"><![CDATA[Conus arterie]]></mc:choice><mc:choice id="3"><![CDATA[Beide bovenstaande]]></mc:choice><mc:choice id="4"><![CDATA[Geen van bovenstaande]]></mc:choice></mc:choices></mc:exercise>
Exercise key:

<mc:key xmlns:mc="http://www.expertcollege.com/mes/multiple-choice/key"><mc:correctanswer id="2"/><mc:defaultexplanation><mc:text><![CDATA[Dit zijn de conus arterie, die het uitstroomkanaal van het rechterventrikel (de conus van de arteria pulmonalis) van bloed voorziet en een tweede tak, die de sinusknoop van bloed voorziet.]]></mc:text></mc:defaultexplanation></mc:key>"""

# Define the messages for stepOne
UserPrompt1 = r"""Exercise body:

<mc:exercise xmlns:mc="http://www.expertcollege.com/mes/multiple-choice/exercise"><mc:question><![CDATA[Theorie:<br />Bij een tekort aan trombocyten (≤150×10<sup>9</sup>/L) spreek je over trombocytopenie.<br /><br />Stelling:<br />Een trombocytopenie ontstaat door .....]]></mc:question><mc:choices><mc:choice id="2"><![CDATA[Een verhoogde afbraak]]></mc:choice><mc:choice id="3"><![CDATA[Een inadequate productie]]></mc:choice><mc:choice id="4"><![CDATA[Beide bovenstaande]]></mc:choice><mc:choice id="5"><![CDATA[Geen van bovenstaande]]></mc:choice></mc:choices></mc:exercise>
Exercise key:

<mc:key xmlns:mc="http://www.expertcollege.com/mes/multiple-choice/key"><mc:correctanswer id="4"/><mc:defaultexplanation><mc:text><![CDATA[]]></mc:text></mc:defaultexplanation></mc:key>
"""
AssistantPrompt1 = r"""Trombocytopenie, een tekort aan trombocyten, ontstaat door: '''zowel een verhoogde afbraak als een inadequate productie'''."""
UserPrompt2 = r"""Exercise body:

<mc:exercise xmlns:mc="http://www.expertcollege.com/mes/multiple-choice/exercise"><mc:question><![CDATA[Stelling:<br />Het buitenste vlies van het pericard wordt het epicard genoemd.]]></mc:question><mc:choices><mc:choice id="1"><![CDATA[Deze stelling is correct]]></mc:choice><mc:choice id="2"><![CDATA[Deze stelling is niet correct]]></mc:choice></mc:choices></mc:exercise>
Exercise key:

<mc:key xmlns:mc="http://www.expertcollege.com/mes/multiple-choice/key"><mc:correctanswer id="2"/><mc:defaultexplanation><mc:text><![CDATA[Het pericard (hartzakje) bestaat uit twee vliezen, namelijk het binnenste vlies (viscerale pericard, ook wel het epicard) en het buitenste vlies (pariëtale pericard).]]></mc:text></mc:defaultexplanation></mc:key>
"""
AssistantPrompt2 = "Het buitenste vlies van het pericard wordt '''het pariëtale pericard''' genoemd."
UserPrompt3 = r"""Exercise body:

<mc:exercise xmlns:mc="http://www.expertcollege.com/mes/multiple-choice/exercise"><mc:question><![CDATA[Theorie:<br />Acute myocardiale ischemie kan optreden bij gebruik van amfetaminen, ecstasy of cocaïne.<br /><br />Vraag:<br />Waardoor treed in dit geval hypotensie op?]]></mc:question><mc:choices><mc:choice id="1"><![CDATA[Door een verhoogde productie van rode bloedcellen]]></mc:choice><mc:choice id="2"><![CDATA[Door de stimulatie van de afgifte van insuline]]></mc:choice><mc:choice id="3"><![CDATA[Beide bovenstaande]]></mc:choice><mc:choice id="4"><![CDATA[Geen van bovenstaande]]></mc:choice></mc:choices></mc:exercise>
Exercise key:

<mc:key xmlns:mc="http://www.expertcollege.com/mes/multiple-choice/key"><mc:correctanswer id="4"/><mc:defaultexplanation><mc:text><![CDATA[Extra info:<br />Hypotensie treedt in dit geval op door acute myocardiale depressie als gevolg van ischemie en een direct toxisch effect van het middel.]]></mc:text></mc:defaultexplanation></mc:key>
"""
AssistantPrompt3 = "In het geval van acute myocardiale ischemie door gebruik van amfetaminen, ecstasy of cocaïne, treedt hypotensie op door: '''acute myocardiale depressie als gevolg van ischemie en een direct toxisch effect van het middel'''."


# Define the messages for stepTwo
UserPrompt21 = "Kennisonderdeel: '''De arteria pulmonalis''' komt rechtstreeks uit het rechterventrikel."
AssistantPrompt21 = "Vraag: Welke slagader komt rechtstreeks uit het rechterventrikel?\nJuiste antwoord: De arteria pulmonalis"
UserPrompt22 = "Kennisonderdeel: Geografische kenmerken in een klantprofiel geven informatie over '''de woonplaats van een klant''', zoals het land, de regio of de stad."
AssistantPrompt22 = "Vraag: Waar geven geografische kenmerken in een klantprofiel informatie over?\nJuiste antwoord: De woonplaats van de klant"

# Define the messages for stepThree
SystemPrompt31 = r"""Je bent een breedgeschoolde professor met veel expertise over de onderwerpen van toetsvragen.

Genereer uitspraken die niet waar zijn, maar geloofwaardige misvattingen over de informatie in de gepresenteerde vraag.

Zorg ervoor dat alle misvattingen daadwerkelijk volledig onwaar zijn in alle gevallen en omstandigheden, maar op een subtiele manier. Ze moeten geloofwaardige variaties op het juiste antwoord presenteren. 
Formuleer je misvattingen overwegend positief, dus vermijd het gebruik van 'geen' en 'niet' en vermijd absoluut/extreem taalgebruik. Zorg dat het taalniveau overeenkomt met het juiste antwoord. 
Geef geen toelichting bij de misvattingen.

Let op: zorg dat je misvattingen:
    - zich strikt richten op de informatie in de vraag, niet op het overkoepelende onderwerp in zijn geheel
    - geloofwaardig zijn voor iemand met basiskennis over het studieonderwerp"""
UserPrompt31 = r"""Studieonderwerp: Het zenuwstelsel
Vraag: Wat maakt het zenuwstelsel onder andere mogelijk? 
Juiste antwoord: Eten, ademen, lopen, en praten"""
AssistantPrompt31 = r"""Misvattingen:
1. Het zenuwstelsel is direct verantwoordelijk voor het opnemen van zuurstof uit de ingeademde lucht.
2. Door het zenuwstelsel kunnen we energie maken uit zonlicht.
3. Het zenuwstelsel maakt het mogelijk om vitamine B op te nemen uit zonlicht.
4. Het zenuwstelsel maakt het mogelijk om het zuurstofniveau in het bloed te meten.
5. Het regelen van de zuurstofbinding aan hemoglobine in de longen wordt mogelijk gemaakt door het zenuwstelsel.
6. Het zenuwstelsel maakt het mogelijk om het suikergehalte in het bloed te regelen."""
UserPrompt32 = r"""Studieonderwerp: Het zenuwstelsel
Vraag: Wat zijn de twee voornaamste zenuwstelsels die we in het lichaam onderscheiden?
Juiste antwoord: Het centraal en perifeer zenuwstelsel"""
AssistantPrompt32 = r"""Misvattingen:
1. In ons lichaam wordt het zenuwstelsel met name onderverdeeld in het autonome en het viscerale zenuwstelsel.
2. We verdelen het zenuwstelsel in ons lichaam in de eerste plaats onder in het cerebrale en het spinale zenuwstelsel.
3. In het menselijk lichaam worden voornamelijk twee zenuwstelsels onderscheiden: het animale zenuwstelsel en het somatische zenuwstelsel.
4. De twee hoofdzenuwstelsels in ons lichaam zijn het motorisch en endocrien systeem.
5. Het zenuwstelsel in het lichaam wordt met name onderverdeeld in het interne en externe zenuwstelsel.
6. Het zenuwstelsel in het menselijk lichaam wordt meestal onderverdeeld in het oppervlakkige en diepe zenuwstelsel.
7. Het zenuwstelsel wordt vaak onderverdeeld in het methische en het hermethische zenuwstelsel.
8. De hoofdindeling van het zenuwstelsel is het voorste en het achterste zenuwstelsel."""
UserPrompt33 = r"""Studieonderwerp: Klantprofielen en marktsegmentatie
Vraag: Bij het opstellen van een klantprofiel, welke soort informatie nemen we daar voornamelijk in mee?
Juiste antwoord: Leeftijd, geslacht, en woonplaats"""
AssistantPrompt33 = r"""Misvattingen:
1. In een klantprofiel worden vooral aankoop- en betalingsgeschiedenis van de klant in detail opgenomen.
2. De afkomst van de klant is onmisbaar bij het opstellen van een klantprofiel.
3. Wanneer we een klantprofiel samenstellen, leggen we de meeste aandacht op hun onderwijsniveau.
4. Een klantprofiel wordt vooral opgesteld op basis van de politieke voorkeuren van de klant.
5. Het persoonlijke inkomen van de klant is één van de belangrijkste factoren bij het vormen van een klantprofiel.
6. De religieuze overtuigingen van een klant zijn het belangrijkst bij het maken van een klantprofiel.
7. Wanneer we een klantprofiel opstellen, geven we vooral voorrang aan de gezondheidsstatus van de klant.
8. Bij het opstellen van een klantprofiel is de voornaamste informatie de carrière/beroep van de klant.
9. De militaire status is onmisbaar bij het opstellen van een klantprofiel."""



# Define the messages for stepFour
SystemPrompt41 = r"""Je bent een breed-geschoolde professor. Op basis van een vraag, antwoord en een lijstje met misvattingen genereer je de meest geloofwaardige, doch incorrecte, afleiders voor een meerkeuzevraag.
De afleiders moeten eenzelfde lengte, grammaticale structuur en taalniveau hebben als het juiste antwoord.
De afleiders moeten geloofwaardig klinken voor iemand die weinig over het onderwerp weet, maar daadwerkelijk volledig onjuist zijn. Ze mogen de vraag op geen enkele manier correct beantwoorden. Zorg dat zij dus het foutieve aspect van de misvatting waarop ze zijn gebaseerd behouden, op een subtiele manier."""
UserPrompt41 = r"""Je bent een expert op het gebied van 'Klantprofielen en marktsegmentatie'. 
Vraag: Welke soort informatie nemen we voornamelijk mee in het opstellen van een klantprofiel? 
Juiste antwoord: Leeftijd, geslacht, en woonplaats 

Misvattingen: 
1. In een klantprofiel worden vooral aankoop- en betalingsgeschiedenis van de klant in detail opgenomen.
2. De afkomst van de klant is onmisbaar bij het opstellen van een klantprofiel.
3. Wanneer we een klantprofiel samenstellen, leggen we de meeste aandacht op hun onderwijsniveau.
4. Een klantprofiel wordt vooral opgesteld op basis van de politieke voorkeuren van de klant.
5. Het inkomen van de klant is één van de belangrijkste factoren bij het vormen van een klantprofiel.
6. De religieuze overtuigingen van een klant zijn het belangrijkst bij het maken van een klantprofiel.
7. Wanneer we een klantprofiel opstellen, geven we vooral voorrang aan de gezondheidsstatus van de klant.
8. Bij het opstellen van een klantprofiel is de voornaamste informatie de carrière of het beroep van de klant.
9. De militaire status is onmisbaar bij het opstellen van een klantprofiel. """
AssistantPrompt41 = r"""Vraag: 
Welke soort informatie nemen we voornamelijk mee in het opstellen van een klantprofiel?

Juiste antwoord:
Leeftijd, geslacht, en woonplaats

Afleiders: 
Aankoop- en betaalgeschiedenis
Opleidingsniveau en politieke voorkeuren
Afkomst, religie, en gezondheidstatus
Informatie over carrière en beroep


"""
UserPrompt42 = r"""Je bent een expert op het gebied van het zenuwstelsel. 
Vraag: Tot welk zenuwstelsel behoort het ruggenmerg?
Juiste antwoord: Het centrale zenuwstelsel

Misvattingen:
1. Het ruggenmerg behoort tot het perifere zenuwstelsel.
2. Het motorische zenuwstelsel is waar het ruggenmerg bijhoort.
3. Het ruggenmerg behoort tot het parasympathisch zenuwstelsel.
4. Het ruggenmerg behoort tot het quadratische zenuwstelsel.
5. Het ruggenmerg behoort tot het craniale zenuwstelsel.
"""
AssistantPrompt42 = r"""Vraag: 
Tot welk zenuwstelsel behoort het ruggenmerg? 

Juiste antwoord: 
Het centrale zenuwstelsel

Afleiders: 
Het perifere zenuwstelsel 
Het motorische zenuwstelsel
Het parasympathisch zenuwstelsel
Het quadratische zenuwstelsel"""

## Define the messages for stepFive
#UserPrompt41 =  r""""""
#AssistantPrompt41 = r""""""
#UserPrompt42 = r""""""
#AssistantPrompt42 = r""""""
#UserPrompt43 = r""""""
#AssistantPrompt43 = r""""""

# Function to make API call
def api_call(messages, temperature=0.9, model="gpt-4"):
    return openai.ChatCompletion.create( 
        messages=messages,
        temperature=temperature,
        model=model
    ).choices[0].message.content

# Function to be called by Gradio interface
def chatbot(input):
    # Check if input is empty
    if not input:
        return manual
    # Check if input text contains '[CDATA'
    if "[CDATA" in input:
    # Step 1: User input and first API call ~5secs
        stepOne = [
            {"role": "system", "content": "You distill a takeaway out of an exercise's question and answer. Mark the answer part in triple quotes '''. Don't do anything else."},
            {"role": "user", "content": UserPrompt1},
            {"role": "assistant", "content": AssistantPrompt1},
            {"role": "user", "content": UserPrompt2},
            {"role": "assistant", "content": AssistantPrompt2},
            {"role": "user", "content": UserPrompt3},
            {"role": "assistant", "content": AssistantPrompt3},
            {"role": "user", "content": input}
        ]
        Takeaway = api_call(stepOne, 0.4)
        strippedTakeaway = Takeaway.replace("'''", '')
    else:
# Skip stepOne and set 'Takeaway' to input
        strippedTakeaway = input.replace("'''", '')
        Takeaway = input
    # Step 2: second API call with first call's output as input ~2secs
    stepTwo = [
        {"role": "system", "content": "Je bent onderwijskundige. Genereer 1 vraag waarmee je de kennis van de student toetst over een specifiek stukje informatie (kennisonderdeel)."},
        {"role": "user", "content": UserPrompt21},
        {"role": "assistant", "content": AssistantPrompt21},
        {"role": "user", "content": UserPrompt22},
        {"role": "assistant", "content": AssistantPrompt22},
        {"role": "user", "content": "Kennisonderdeel: " + Takeaway}
    ]
    QandA = api_call(stepTwo, 0.5, "gpt-3.5-turbo")

    # Split the QandA string into question and answer parts
    lines = QandA.split('\n')
    # Isolate just the question and answer 
    question = lines[0].split('Vraag: ')[1].strip()
    answer = lines[1].split('Juiste antwoord: ')[1].strip().rstrip(".")

    # Step 3: next API call with previous call's output as input ~21secs
    stepThree = [
        {"role": "system", "content": SystemPrompt31},
        {"role": "user", "content": UserPrompt31},
        {"role": "assistant", "content": AssistantPrompt31},
        {"role": "user", "content": UserPrompt32},
        {"role": "assistant", "content": AssistantPrompt32},
        {"role": "user", "content": QandA}
    ]
    misvattingen = api_call(stepThree)
    
#Step 4: ALL elements next API call with previous call's output as input ~23secs
    stepFour = [
        {"role": "system", "content": SystemPrompt41},
        {"role": "user", "content": UserPrompt41},
        {"role": "assistant", "content": AssistantPrompt41},
        {"role": "user", "content": UserPrompt42},
        {"role": "assistant", "content": AssistantPrompt42},
        {"role": "user", "content": "Je bent medisch expert.\n" + QandA + "\n\n" + misvattingen}
    ]
    BOTA_mc_elements = api_call(stepFour, 0.7)

    # Split the BOTA_mc_elements string by lines
    lines = BOTA_mc_elements.split('\n')

    # Find the index where "Afleiders:" appears
    distractors_index = -1  # Initialize to -1 as a sentinel value
    for i, line in enumerate(lines):
        if line.strip() == "Afleiders:":
            distractors_index = i
            break

    if distractors_index != -1:
       # Extract the afleiders into the distractors list and remove any trailing periods
        distractors = [line.rstrip('.').strip() for line in lines[distractors_index + 1:] if line.strip()]
    else:
        # Handle the case where "Afleiders:" is not found
        distractors = []
        distractors.append("Geen afleiders gevonden. Herlaad de pagina, klik zonder input op 'Submit' voor instructies, en probeer opnieuw. Gaat het een tweede keer mis? Stuur Ben ten Berge een berichtje met je input.")
        distractors.append("Geen afleiders gevonden. Herlaad de pagina, klik zonder input op 'Submit' voor instructies, en probeer opnieuw. Gaat het een tweede keer mis? Stuur Ben ten Berge een berichtje met je input.")

    # Generate the two versions of 'Beide bovenstaande' type
    exercise_1 = f"Vraag:\n{question}\n\n{answer}   ✔\n{distractors[0]}\n{distractors[1]}\n{distractors[2]}\n\n\n\n---------------------\nBonus-afleider:\n{distractors[3]}\n\n---------------------\nOf maak er een 'Beide bovenstaande'-vraag van:\nBeide bovenstaande\nGeen van bovenstaande\n\nExtra info:\n{Takeaway}"
    exercise_2 = f"Vraag:\n{question}\n\n{distractors[0]}\n{answer}   ✔\n{distractors[1]}\n{distractors[2]}\n\n\n\n---------------------\nBonus-afleider:\n{distractors[3]}\n\n---------------------\nOf maak er een 'Beide bovenstaande'-vraag van:\nBeide bovenstaande\nGeen van bovenstaande\n\nExtra info:\n{Takeaway}"
    exercise_3 = f"Vraag:\n{question}\n\n{distractors[0]}\n{distractors[1]}\n{answer}   ✔\n{distractors[2]}\n\n\n\n---------------------\nBonus-afleider:\n{distractors[3]}\n\n---------------------\nOf maak er een 'Beide bovenstaande'-vraag van:\nBeide bovenstaande\nGeen van bovenstaande\n\nExtra info:\n{Takeaway}"
    exercise_4 = f"Vraag:\n{question}\n\n{distractors[0]}\n{distractors[1]}\n{distractors[2]}\n{answer}   ✔\n\n\n\n---------------------\nBonus-afleider:\n{distractors[3]}\n\n---------------------\nOf maak er een 'Beide bovenstaande'-vraag van:\nBeide bovenstaande\nGeen van bovenstaande\n\nExtra info:\n{Takeaway}"
    
    # Define the probabilities
    probabilities = [0.25, 0.25, 0.25, 0.25]  # 25% each (dit kan ongetwijfeld makkelijker en beter.. #quickfix)
    # Randomly choose between OneTrue and NoneTrue based on the probabilities
    random_version = random.choices([exercise_1, exercise_2, exercise_3, exercise_4], weights=probabilities, k=1)[0]

    return random_version
   

inputs = gr.Textbox(lines=7, label="Input")
outputs = gr.Textbox(label="Output")

# Create the Gradio interface with HTML-formatted output
iface = gr.Interface(
    fn=chatbot,
    inputs=inputs,
    outputs=outputs,
    title="Leerdoel naar standaard 'MC-opgave' [v1]",
    description="Voer een leerdoel in en druk op 'Submit'.",
    theme="compact",
    port=7862
)

iface.launch(share=True)