"""
Dataset 5: Multilingual Healthcare Communication
AI Healthcare Navigation Assistant - Synthetic Data Generator
Generates 5,000 multilingual healthcare phrase records.
"""

import csv
import random
import uuid

random.seed(42)

PHRASES = {
    "Emergency": [
        ("I need emergency help.", "Necesito ayuda de emergencia.", "J'ai besoin d'aide d'urgence.",
         "Preciso de ajuda de emergência.", "أحتاج إلى مساعدة طارئة.", "我需要紧急帮助。", "緊急の助けが必要です。"),
        ("Call 911 please.", "Llame al 911 por favor.", "Appelez le 911 s'il vous plaît.",
         "Ligue para o 911, por favor.", "اتصل بـ 911 من فضلك.", "请拨打911。", "911に電話してください。"),
        ("This is an emergency.", "Esto es una emergencia.", "C'est une urgence.",
         "Isso é uma emergência.", "هذه حالة طارئة.", "这是紧急情况。", "これは緊急事態です。"),
        ("I need an ambulance.", "Necesito una ambulancia.", "J'ai besoin d'une ambulance.",
         "Preciso de uma ambulância.", "أحتاج إلى سيارة إسعاف.", "我需要救护车。", "救急車が必要です。"),
        ("Help me, I am very sick.", "Ayúdeme, estoy muy enfermo/a.", "Aidez-moi, je suis très malade.",
         "Ajude-me, estou muito doente.", "ساعدني، أنا مريض جداً.", "救救我，我病得很重。", "助けてください、とても具合が悪いです。"),
    ],
    "Symptoms": [
        ("I have a headache.", "Tengo dolor de cabeza.", "J'ai mal à la tête.",
         "Tenho dor de cabeça.", "عندي صداع.", "我头疼。", "頭痛がします。"),
        ("I have a fever.", "Tengo fiebre.", "J'ai de la fièvre.",
         "Tenho febre.", "عندي حمى.", "我发烧了。", "熱があります。"),
        ("I feel dizzy.", "Me siento mareado/a.", "Je me sens étourdi(e).",
         "Estou tonto/a.", "أشعر بدوار.", "我感到头晕。", "めまいがします。"),
        ("I have chest pain.", "Tengo dolor en el pecho.", "J'ai des douleurs à la poitrine.",
         "Tenho dor no peito.", "عندي ألم في الصدر.", "我胸口疼。", "胸が痛いです。"),
        ("I have difficulty breathing.", "Tengo dificultad para respirar.", "J'ai du mal à respirer.",
         "Tenho dificuldade para respirar.", "أجد صعوبة في التنفس.", "我呼吸困难。", "呼吸が苦しいです。"),
        ("I have abdominal pain.", "Tengo dolor de estómago.", "J'ai mal au ventre.",
         "Tenho dor de estômago.", "عندي ألم في البطن.", "我肚子疼。", "腹痛があります。"),
        ("I am vomiting.", "Estoy vomitando.", "Je vomis.",
         "Estou vomitando.", "أنا أتقيأ.", "我在呕吐。", "吐いています。"),
        ("I have diarrhea.", "Tengo diarrea.", "J'ai la diarrhée.",
         "Tenho diarreia.", "عندي إسهال.", "我拉肚子。", "下痢をしています。"),
        ("I have a rash.", "Tengo sarpullido.", "J'ai une éruption cutanée.",
         "Tenho uma erupção cutânea.", "عندي طفح جلدي.", "我身上起疹子了。", "発疹があります。"),
        ("I have swelling.", "Tengo hinchazón.", "J'ai un gonflement.",
         "Tenho inchaço.", "عندي تورم.", "我有肿胀。", "腫れがあります。"),
        ("I am allergic to penicillin.", "Soy alérgico/a a la penicilina.", "Je suis allergique à la pénicilline.",
         "Sou alérgico/a à penicilina.", "أنا حساس للبنسلين.", "我对青霉素过敏。", "ペニシリンにアレルギーがあります。"),
        ("I have a food allergy.", "Tengo alergia alimentaria.", "J'ai une allergie alimentaire.",
         "Tenho alergia alimentar.", "عندي حساسية من طعام.", "我有食物过敏。", "食物アレルギーがあります。"),
    ],
    "Medication": [
        ("I lost my medication.", "Perdí mi medicamento.", "J'ai perdu mes médicaments.",
         "Perdi meu medicamento.", "فقدت دوائي.", "我丢失了我的药。", "薬をなくしました。"),
        ("I need a prescription refill.", "Necesito renovar mi receta.", "J'ai besoin d'un renouvellement d'ordonnance.",
         "Preciso renovar minha receita.", "أحتاج إلى تجديد وصفتي الطبية.", "我需要续药。", "処方の更新が必要です。"),
        ("I take this medication daily.", "Tomo este medicamento a diario.", "Je prends ce médicament quotidiennement.",
         "Tomo este medicamento diariamente.", "أتناول هذا الدواء يومياً.", "我每天服用这种药。", "毎日この薬を飲んでいます。"),
        ("Where can I find a pharmacy?", "¿Dónde puedo encontrar una farmacia?", "Où puis-je trouver une pharmacie?",
         "Onde posso encontrar uma farmácia?", "أين يمكنني العثور على صيدلية؟", "哪里有药店？", "薬局はどこですか？"),
        ("Do you have this medication?", "¿Tiene este medicamento?", "Avez-vous ce médicament?",
         "Você tem este medicamento?", "هل لديك هذا الدواء؟", "你们有这种药吗？", "この薬はありますか？"),
        ("I am diabetic and need insulin.", "Soy diabético/a y necesito insulina.", "Je suis diabétique et j'ai besoin d'insuline.",
         "Sou diabético/a e preciso de insulina.", "أنا مصاب بالسكري وأحتاج إلى الأنسولين.", "我是糖尿病患者，需要胰岛素。", "糖尿病でインスリンが必要です。"),
        ("I have an EpiPen for severe allergies.", "Tengo un EpiPen para alergias graves.", "J'ai un EpiPen pour les allergies sévères.",
         "Tenho uma EpiPen para alergias graves.", "لدي قلم إبينفرين للحساسية الشديدة.", "我有用于严重过敏的肾上腺素笔。", "重度アレルギー用のエピペンを持っています。"),
    ],
    "Navigation": [
        ("Where is the nearest urgent care center?", "¿Dónde está el centro de atención urgente más cercano?",
         "Où se trouve le centre de soins urgents le plus proche?", "Onde fica o centro de atendimento urgente mais próximo?",
         "أين أقرب مركز للرعاية العاجلة؟", "最近的紧急护理中心在哪里？", "最寄りの緊急ケアセンターはどこですか？"),
        ("Where is the nearest emergency room?", "¿Dónde está la sala de emergencias más cercana?",
         "Où se trouve la salle d'urgence la plus proche?", "Onde fica a sala de emergência mais próxima?",
         "أين أقرب غرفة طوارئ؟", "最近的急诊室在哪里？", "最寄りの救急室はどこですか？"),
        ("Is there a doctor who speaks my language?", "¿Hay un médico que hable mi idioma?",
         "Y a-t-il un médecin qui parle ma langue?", "Há um médico que fala minha língua?",
         "هل يوجد طبيب يتحدث لغتي؟", "有会说我语言的医生吗？", "私の言語を話す医師はいますか？"),
        ("How do I get to the hospital?", "¿Cómo llego al hospital?", "Comment est-ce que j'arrive à l'hôpital?",
         "Como chego ao hospital?", "كيف أصل إلى المستشفى؟", "我怎么去医院？", "病院にはどうやって行けばいいですか？"),
        ("I need a telehealth appointment.", "Necesito una consulta de telemedicina.", "J'ai besoin d'un rendez-vous en téléconsultation.",
         "Preciso de uma consulta de telemedicina.", "أحتاج إلى موعد مع طبيب عبر الإنترنت.", "我需要远程医疗预约。", "遠隔医療の予約が必要です。"),
    ],
    "Insurance": [
        ("I have travel insurance.", "Tengo seguro de viaje.", "J'ai une assurance voyage.",
         "Tenho seguro de viagem.", "لدي تأمين سفر.", "我有旅游保险。", "旅行保険に加入しています。"),
        ("I do not have insurance.", "No tengo seguro.", "Je n'ai pas d'assurance.",
         "Não tenho seguro.", "ليس لدي تأمين.", "我没有保险。", "保険に入っていません。"),
        ("Can I pay out of pocket?", "¿Puedo pagar de mi bolsillo?", "Puis-je payer de ma poche?",
         "Posso pagar do meu próprio bolso?", "هل يمكنني الدفع من جيبي الخاص؟", "我可以自费吗？", "自費で支払えますか？"),
        ("What is the cost of this visit?", "¿Cuánto cuesta esta consulta?", "Quel est le coût de cette consultation?",
         "Qual é o custo desta consulta?", "ما هي تكلفة هذه الزيارة؟", "这次就诊需要多少钱？", "この受診の費用はいくらですか？"),
        ("Do you accept international insurance?", "¿Aceptan seguro internacional?", "Acceptez-vous une assurance internationale?",
         "Vocês aceitam seguro internacional?", "هل تقبلون التأمين الدولي؟", "你们接受国际保险吗？", "海外の保険は使えますか？"),
    ],
    "Communication": [
        ("I do not speak English.", "No hablo inglés.", "Je ne parle pas anglais.",
         "Não falo inglês.", "لا أتكلم الإنجليزية.", "我不会说英语。", "英語が話せません。"),
        ("Do you have an interpreter?", "¿Tiene un intérprete?", "Avez-vous un interprète?",
         "Você tem um intérprete?", "هل لديك مترجم؟", "你们有翻译吗？", "通訳はいますか？"),
        ("Can you write it down please?", "¿Puede escribirlo por favor?", "Pouvez-vous l'écrire s'il vous plaît?",
         "Pode escrever, por favor?", "هل يمكنك كتابته من فضلك؟", "能写下来吗？", "書いていただけますか？"),
        ("Please speak slowly.", "Por favor hable despacio.", "Parlez lentement s'il vous plaît.",
         "Por favor fale devagar.", "من فضلك تحدث ببطء.", "请说慢点。", "ゆっくり話してください。"),
        ("I do not understand.", "No entiendo.", "Je ne comprends pas.",
         "Não entendo.", "لا أفهم.", "我不明白。", "わかりません。"),
    ],
}

LANGUAGE_MAP = {
    0: "English", 1: "Spanish", 2: "French", 3: "Portuguese",
    4: "Arabic", 5: "Chinese", 6: "Japanese"
}


def generate_multilingual_phrases(n=5000):
    records = []
    for category, phrase_tuples in PHRASES.items():
        for phrase_tuple in phrase_tuples:
            for lang_idx, lang_name in LANGUAGE_MAP.items():
                records.append({
                    "phrase_id": str(uuid.uuid4()),
                    "language": lang_name,
                    "phrase": phrase_tuple[lang_idx],
                    "english_translation": phrase_tuple[0],
                    "category": category,
                })

    # Fill to n by sampling
    while len(records) < n:
        category = random.choice(list(PHRASES.keys()))
        phrase_tuple = random.choice(PHRASES[category])
        lang_idx = random.randint(0, 6)
        lang_name = LANGUAGE_MAP[lang_idx]
        records.append({
            "phrase_id": str(uuid.uuid4()),
            "language": lang_name,
            "phrase": phrase_tuple[lang_idx],
            "english_translation": phrase_tuple[0],
            "category": category,
        })

    random.shuffle(records)
    return records[:n]


def write_csv(records, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
    print(f"✅  Wrote {len(records):,} records → {filename}")


if __name__ == "__main__":
    data = generate_multilingual_phrases(5000)
    write_csv(data, "/mnt/user-data/outputs/multilingual_phrases.csv")
