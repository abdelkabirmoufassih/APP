from flask import Flask, render_template, request
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

app = Flask(__name__)

questions = {
    "fr":[{
        "question": "1-Quelles sont les objets et les produits interdits avant d'accèder à la station ?",
        "options": ["Les objets en verre", "Ustensiles en plastique", " Médicament", "Tomate  et poivrons"],
        "correct_answers": ["Les objets en verre", "Tomate  et poivrons"],
    },
    {
        "question": "2-Quelles sont les interdictions à l'intérieur de la station ?",
        "options": ["Les bijoux", "Barbe non protégée", "Les produits alimentaires /allergènes", "Les lunettes solaires ou lentilles brisées ou fissurées"],
        "correct_answers": ["Les bijoux", "Barbe non protégée", "Les produits alimentaires /allergènes", "Les lunettes solaires ou lentilles brisées ou fissurées"]
    },
    {
        "question": "3- Quelles sont les caractéristiques d'une tenue de travail conforme ?  ",
        "options": ["Blouse modifiée/Chaussures ouvertes", "Blouse couverant les vêtements personnels et propre", "Couverture des cheveux foulard ou casquette", "Des vêtements avec des motifs de décoration(pierre/istrasses)"],
        "correct_answers": ["Blouse couverant les vêtements personnels et propre", "Couverture des cheveux foulard ou casquette"]
    },
    {
        "question": "4- Comment doit être l'arrangement des affaires dans les casiers ? ",
        "options": ["Mettre tout dans un même sac", "Séparer entre la tenue de travail et autre effet personnel", "Mettre les aliments au dessous des vêtements", "Mettre des produits en verre au dessus"],
        "correct_answers": ["Séparer entre la tenue de travail et autre effet personnel"]
    },
    {
        "question": "5- Que doit on faire en cas de présence d'un corps étranger ? ",
        "options": ["Arrêter la machine et éliminer le corps étranger (nuisible)", "Informer le responsable puis arrêter la machine", "Arrêter la machine puis informer le responsable", "Le jeter vers la poubelle"],
        "correct_answers": ["Arrêter la machine et éliminer le corps étranger (nuisible)", "Arrêter la machine puis informer le responsable"]
    },
    {
        "question": "6- Que doit faire en cas d'accident/présence de substance corporelles ?",
        "options": ["En cas de Epistaxis je doit rester à ma place", "En cas d'une blessure sanglante je dois rester à ma place et j'attend les premiers secours", "En cas de vomissement aviser l'infirmerie", "En cas de présence des substances corporelles je dois rester a ma place et suivre les consignes de responsable"],
        "correct_answers": ["En cas de Epistaxis je doit rester à ma place", "En cas d'une blessure sanglante je dois rester à ma place et j'attend les premiers secours", "En cas de présence des substances corporelles je dois rester a ma place et suivre les consignes de responsable"]
    },
    {
        "question": "7- Quel sont les règles d'hygiène a respecter lors d'utilisation des sanitaires ?",
        "options": ["Enlever la blouse seulement", "Enlever toute la tenue de travail", "Désinfecter les mains avant l'enter", "Lavager et désinfection des mains après l'utilisation et avant de porter la tenue du travail"],
        "correct_answers": ["Enlever toute la tenue de travail", "Lavager et désinfection des mains après l'utilisation et avant de porter la tenue du travail"]
    },
    {
        "question": "8- Quand dois-je changer les gants ?",
        "options": ["Après le changement de chantier, Après l'utilisation sanitaire", "Après 1 heure de travail", "Gants sale et déchirées", "Chaque fois"],
        "correct_answers": ["Après le changement de chantier, Après l'utilisation sanitaire", "Gants sale et déchirées"]
    },
    {
        "question": "9- Que dois-je faire avant d'entrer à la station ?",
        "options": ["Laver son visage", "Laver, sécher et désinfecter les mains et désinfecter les semelles des chaussures", "Fermer les portes après chaque utilisation", "pas nécessaire de désinfecter les mains. Le lavage est suffisant"],
        "correct_answers": ["Laver, sécher et désinfecter les mains et désinfecter les semelles des chaussures", "Fermer les portes après chaque utilisation"]
    },
    {
        "question": "10- Que dois-je faire au cas de détection des nuisibles ?",
        "options": ["Informer le service concerné", "Eliminer le nuisible puis informer le responsable le plus proche", "Arrêt de la machine immédiatement et informer le responsable de la ligne", "Laisser les insectes et éliminer les animaux"],
        "correct_answers": ["Informer le service concerné", "Eliminer le nuisible puis informer le responsable le plus proche", "Arrêt de la machine immédiatement et informer le responsable de la ligne"]
    },
    {
        "question": "11- Quel-est l'action à faire en cas de présence d'une personne étrangère à l'intérieur de station ?",
        "options": ["Avertir la personne étranger", "Informer le responsable le plus proche", "Informer l'agent de sécurité", "Je ne suis pas concerné pour faire cette action"],
        "correct_answers": ["Informer le responsable le plus proche", "Informer l'agent de sécurité"]
    },
    {
        "question": "12- Quel-est l'objectif de la présence des différentes couleurs des blouses à la station ?",
        "options": ["L'identification des personnes par service", "Détection rapidement des personnes étrangères", "Protéger les personnes et le produit", "Pas d'objectif"],
        "correct_answers": ["L'identification des personnes par service", "Détection rapidement des personnes étrangères", "Protéger les personnes et le produit"]
    },
    {
        "question": "13- Quel sont les risques physique ?",
        "options": ["Débris de peinture", "Les bijoux", "La graisse", "Traces des nuisibles"],
        "correct_answers": ["Débris de peinture", "Les bijoux"]
    },
    {
        "question": "14- Quel sont les risques chimiques ?",
        "options": ["La peinture", "Morceaux de plastique", "Produit de nettoyage", "Produits dégraissants des machines"],
        "correct_answers": ["La peinture","Produit de nettoyage", "Produits dégraissants des machines"]
    },
    {
        "question": "15- Quel sont les risques biologiques ?",
        "options": ["Substance corporelle", "Pourriture sur produit", "Les maladies contagieuses", "les bijoux"],
        "correct_answers": ["Substance corporelle", "Pourriture sur produit", "Les maladies contagieuses"]
    },
    {
        "question": "16- Quelles est votre réaction si quelqu'un de votre équipe a fait un comportement non sanitaire ? ",
        "options": ["Sensibilisation immédiatement", "Aviser le service concerné pour demande d'une formation", "Pas d'action", "Ce n'est pas mon périmètre"],
        "correct_answers": ["Sensibilisation immédiatement", "Aviser le service concerné pour demande d'une formation"]
    },
    {
        "question": "17- Quel sont les instructions à suivre en cas d'accompagnement d'un visiteur ou prestataire ? ",
        "options": ["Expliquer, et signer le formulaire visiteurs", "Porter les bijoux et des objets personnels", "Porter une tenue dédiée aux visiteurs", "Respecter les règles sanitaires aux visiteurs"],
        "correct_answers": ["Expliquer, et signer le formulaire visiteurs","Porter une tenue dédiée aux visiteurs", "Respecter les règles sanitaires aux visiteurs"]
    }],
"en":[{
    "question": "1- What are the prohibited objects and products before entering the station?",
    "options": ["Glass objects", "Plastic utensils", "Medicine", "Tomatoes and peppers"],
    "correct_answers": ["Glass objects", "Tomatoes and peppers"]
},
{
    "question": "2- What are the prohibitions inside the station?",
    "options": ["Jewelry", "Unprotected beard", "Food products/allergens", "Broken or cracked sunglasses or lenses"],
    "correct_answers": ["Jewelry", "Unprotected beard", "Food products/allergens", "Broken or cracked sunglasses or lenses"]
},
{
    "question": "3- What are the characteristics of compliant work attire?",
    "options": ["Modified coat/Open shoes", "Coat covering personal clothes and clean", "Hair covered with scarf or cap", "Clothes with decorative patterns (stones/sequins)"],
    "correct_answers": ["Coat covering personal clothes and clean", "Hair covered with scarf or cap"]
},
{
    "question": "4- How should items be arranged in the lockers?",
    "options": ["Put everything in the same bag", "Separate work attire from other personal items", "Put food under the clothes", "Place glass products on top"],
    "correct_answers": ["Separate work attire from other personal items"]
},
{
    "question": "5- What should be done in case of the presence of a foreign object?",
    "options": ["Stop the machine and eliminate the foreign object (pest)", "Inform the responsible person then stop the machine", "Stop the machine then inform the responsible person", "Throw it in the trash"],
    "correct_answers": ["Stop the machine and eliminate the foreign object (pest)", "Stop the machine then inform the responsible person"]
},
{
    "question": "6- What should be done in case of an accident/presence of bodily substances?",
    "options": ["In case of epistaxis, stay in place", "In case of a bleeding wound, stay in place and wait for first aid", "In case of vomiting, notify the infirmary", "In case of the presence of bodily substances, stay in place and follow the responsible person's instructions"],
    "correct_answers": ["In case of epistaxis, stay in place", "In case of a bleeding wound, stay in place and wait for first aid", "In case of the presence of bodily substances, stay in place and follow the responsible person's instructions"]
},
{
    "question": "7- What are the hygiene rules to follow when using the restrooms?",
    "options": ["Remove the coat only", "Remove all work attire", "Disinfect hands before entering", "Wash and disinfect hands after use and before wearing work attire"],
    "correct_answers": ["Remove all work attire", "Wash and disinfect hands after use and before wearing work attire"]
},
{
    "question": "8- When should gloves be changed?",
    "options": ["After changing the worksite, after using the restroom", "After 1 hour of work", "Dirty and torn gloves", "Every time"],
    "correct_answers": ["After changing the worksite, after using the restroom", "Dirty and torn gloves"]
},
{
    "question": "9- What should I do before entering the station?",
    "options": ["Wash your face", "Wash, dry and disinfect hands and disinfect shoe soles", "Close the doors after each use", "No need to disinfect hands. Washing is sufficient"],
    "correct_answers": ["Wash, dry and disinfect hands and disinfect shoe soles", "Close the doors after each use"]
},
{
    "question": "10- What should I do in case of pest detection?",
    "options": ["Inform the concerned service", "Eliminate the pest then inform the nearest responsible person", "Stop the machine immediately and inform the line manager", "Leave insects and eliminate animals"],
    "correct_answers": ["Inform the concerned service", "Eliminate the pest then inform the nearest responsible person", "Stop the machine immediately and inform the line manager"]
},
{
    "question": "11- What action should be taken in case of the presence of a foreign person inside the station?",
    "options": ["Warn the foreign person", "Inform the nearest responsible person", "Inform the security guard", "I am not concerned with this action"],
    "correct_answers": ["Inform the nearest responsible person", "Inform the security guard"]
},
{
    "question": "12- What is the purpose of having different colored coats in the station?",
    "options": ["Identifying people by service", "Quickly detecting foreign persons", "Protecting people and the product", "No purpose"],
    "correct_answers": ["Identifying people by service", "Quickly detecting foreign persons", "Protecting people and the product"]
},
{
    "question": "13- What are the physical risks?",
    "options": ["Paint debris", "Jewelry", "Grease", "Pest traces"],
    "correct_answers": ["Paint debris", "Jewelry"]
},
{
    "question": "14- What are the chemical risks?",
    "options": ["Paint", "Plastic pieces", "Cleaning products", "Degreasing products for machines"],
    "correct_answers": ["Paint", "Cleaning products", "Degreasing products for machines"]
},
{
    "question": "15- What are the biological risks?",
    "options": ["Bodily substances", "Rotten product", "Contagious diseases", "Jewelry"],
    "correct_answers": ["Bodily substances", "Rotten product", "Contagious diseases"]
},
{
    "question": "16- What is your reaction if someone on your team exhibits unsanitary behavior?",
    "options": ["Immediate awareness", "Notify the concerned service for a training request", "No action", "It's not my responsibility"],
    "correct_answers": ["Immediate awareness", "Notify the concerned service for a training request"]
},
{
    "question": "17- What are the instructions to follow when accompanying a visitor or service provider?",
    "options": ["Explain and sign the visitor form", "Wear jewelry and personal items", "Wear a dedicated visitor outfit", "Respect sanitary rules for visitors"],
    "correct_answers": ["Explain and sign the visitor form", "Wear a dedicated visitor outfit", "Respect sanitary rules for visitors"]
}],
"ar":[{
    "question": "1- ما هي الأشياء والمنتجات المحظورة قبل الدخول إلى المحطة؟",
    "options": ["الأشياء الزجاجية", "الأدوات البلاستيكية", "الأدوية", "الطماطم والفلفل"],
    "correct_answers": ["الأشياء الزجاجية", "الطماطم والفلفل"]
},
{
    "question": "2- ما هي المحظورات داخل المحطة؟",
    "options": ["المجوهرات", "اللحية غير المحمية", "المنتجات الغذائية / المواد المسببة للحساسية", "النظارات الشمسية المكسورة أو المتشققة"],
    "correct_answers": ["المجوهرات", "اللحية غير المحمية", "المنتجات الغذائية / المواد المسببة للحساسية", "النظارات الشمسية المكسورة أو المتشققة"]
},
{
    "question": "3- ما هي خصائص الزي المناسب للعمل؟",
    "options": ["معطف معدل/أحذية مفتوحة", "معطف يغطي الملابس الشخصية ونظيف", "تغطية الشعر بوشاح أو قبعة", "ملابس بنقوش زخرفية (أحجار/ترتر)"],
    "correct_answers": ["معطف يغطي الملابس الشخصية ونظيف", "تغطية الشعر بوشاح أو قبعة"]
},
{
    "question": "4- كيف يجب ترتيب الأغراض في الخزائن؟",
    "options": ["وضع كل شيء في حقيبة واحدة", "فصل الزي العمل عن الأشياء الشخصية الأخرى", "وضع الطعام تحت الملابس", "وضع المنتجات الزجاجية فوق"],
    "correct_answers": ["فصل الزي العمل عن الأشياء الشخصية الأخرى"]
},
{
    "question": "5- ماذا يجب أن يتم في حال وجود جسم غريب؟",
    "options": ["إيقاف الماكينة وإزالة الجسم الغريب (الآفة)", "إبلاغ المسؤول ثم إيقاف الماكينة", "إيقاف الماكينة ثم إبلاغ المسؤول", "رميه في القمامة"],
    "correct_answers": ["إيقاف الماكينة وإزالة الجسم الغريب (الآفة)", "إيقاف الماكينة ثم إبلاغ المسؤول"]
},
{
    "question": "6- ماذا يجب أن يتم في حالة الحادث/وجود مواد جسدية؟",
    "options": ["في حالة النزيف الأنفي، البقاء في مكانك", "في حالة الجرح النازف، البقاء في مكانك وانتظار الإسعافات الأولية", "في حالة التقيؤ، إبلاغ العيادة", "في حالة وجود مواد جسدية، البقاء في مكانك واتباع تعليمات المسؤول"],
    "correct_answers": ["في حالة النزيف الأنفي، البقاء في مكانك", "في حالة الجرح النازف، البقاء في مكانك وانتظار الإسعافات الأولية", "في حالة وجود مواد جسدية، البقاء في مكانك واتباع تعليمات المسؤول"]
},
{
    "question": "7- ما هي قواعد النظافة التي يجب اتباعها عند استخدام الحمامات؟",
    "options": ["خلع المعطف فقط", "خلع كامل زي العمل", "تطهير اليدين قبل الدخول", "غسل وتطهير اليدين بعد الاستخدام وقبل ارتداء زي العمل"],
    "correct_answers": ["خلع كامل زي العمل", "غسل وتطهير اليدين بعد الاستخدام وقبل ارتداء زي العمل"]
},
{
    "question": "8- متى يجب تغيير القفازات؟",
    "options": ["بعد تغيير مكان العمل، بعد استخدام الحمام", "بعد ساعة من العمل", "قفازات متسخة وممزقة", "كل مرة"],
    "correct_answers": ["بعد تغيير مكان العمل، بعد استخدام الحمام", "قفازات متسخة وممزقة"]
},
{
    "question": "9- ماذا يجب أن أفعل قبل الدخول إلى المحطة؟",
    "options": ["غسل وجهك", "غسل وتجفيف وتطهير اليدين وتطهير نعل الأحذية", "إغلاق الأبواب بعد كل استخدام", "ليس من الضروري تطهير اليدين. الغسل يكفي"],
    "correct_answers": ["غسل وتجفيف وتطهير اليدين وتطهير نعل الأحذية", "إغلاق الأبواب بعد كل استخدام"]
},
{
    "question": "10- ماذا يجب أن أفعل في حالة اكتشاف آفات؟",
    "options": ["إبلاغ الخدمة المعنية", "إزالة الآفة ثم إبلاغ أقرب مسؤول", "إيقاف الماكينة فوراً وإبلاغ مدير الخط", "ترك الحشرات وإزالة الحيوانات"],
    "correct_answers": ["إبلاغ الخدمة المعنية", "إزالة الآفة ثم إبلاغ أقرب مسؤول", "إيقاف الماكينة فوراً وإبلاغ مدير الخط"]
},
{
    "question": "11- ما هو الإجراء الذي يجب اتخاذه في حالة وجود شخص غريب داخل المحطة؟",
    "options": ["تحذير الشخص الغريب", "إبلاغ أقرب مسؤول", "إبلاغ حارس الأمن", "لست معنيًا بهذا الإجراء"],
    "correct_answers": ["إبلاغ أقرب مسؤول", "إبلاغ حارس الأمن"]
},
{
    "question": "12- ما هو الهدف من وجود ألوان مختلفة للمعاطف في المحطة؟",
    "options": ["تحديد الأشخاص حسب الخدمة", "الكشف السريع عن الأشخاص الغريبين", "حماية الأشخاص والمنتج", "لا هدف"],
    "correct_answers": ["تحديد الأشخاص حسب الخدمة", "الكشف السريع عن الأشخاص الغريبين", "حماية الأشخاص والمنتج"]
},
{
    "question": "13- ما هي المخاطر الفيزيائية؟",
    "options": ["شظايا الطلاء", "المجوهرات", "الشحم", "آثار الآفات"],
    "correct_answers": ["شظايا الطلاء", "المجوهرات"]
},
{
    "question": "14- ما هي المخاطر الكيميائية؟",
    "options": ["الطلاء", "قطع البلاستيك", "منتجات التنظيف", "منتجات إزالة الشحوم للماكينات"],
    "correct_answers": ["الطلاء", "منتجات التنظيف", "منتجات إزالة الشحوم للماكينات"]
},
{
    "question": "15- ما هي المخاطر البيولوجية؟",
    "options": ["المواد الجسدية", "المنتج الفاسد", "الأمراض المعدية", "المجوهرات"],
    "correct_answers": ["المواد الجسدية", "المنتج الفاسد", "الأمراض المعدية"]
},
{
    "question": "16- ما هو رد فعلك إذا قام شخص من فريقك بسلوك غير صحي؟",
    "options": ["التوعية الفورية", "إبلاغ الخدمة المعنية لطلب تدريب", "لا يوجد إجراء", "ليس من مسؤوليتي"],
    "correct_answers": ["التوعية الفورية", "إبلاغ الخدمة المعنية لطلب تدريب"]
},
{
    "question": "17- ما هي التعليمات التي يجب اتباعها عند مرافقة زائر أو مزود خدمة؟",
    "options": ["شرح وتوقيع نموذج الزائرين", "ارتداء المجوهرات والأشياء الشخصية", "ارتداء زي مخصص للزائرين", "احترام قواعد النظافة للزائرين"],
    "correct_answers": ["شرح وتوقيع نموذج الزائرين", "ارتداء زي مخصص للزائرين", "احترام قواعد النظافة للزائرين"]
}]}

@app.route('/')
def home():
    return render_template('Landing.html')

@app.route('/quiz', methods=['POST'])
def quiz():
    language= request.form['language']
    if language == "en":
        return render_template('quiz_en.html', questions=questions[language], enumerate=enumerate)
    elif language == "fr":
        return render_template('quiz_fr.html', questions=questions[language], enumerate=enumerate)
    elif language == "ar":
        return render_template('quiz_ar.html', questions=questions[language], enumerate=enumerate)
    else: 
        return("language not supported",404)
    
@app.route('/submit', methods=['POST'])
def submit():
    total_correct = 0
    total_wrong = 0
    language=request.form["language"]
    total_possible = sum(len(q["correct_answers"]) for q in questions[language])

    
    emp_id = request.form.get('emp_id')
    cin = request.form.get('cin')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')

    for i, question in enumerate(questions[language]):
        selected_options = request.form.getlist(f'question-{i}')
        correct_answers = set(question["correct_answers"])
        selected_set = set(selected_options)

        correct_selected = len(correct_answers.intersection(selected_set))
        wrong_selected = len(selected_set - correct_answers)

        total_correct += correct_selected
        total_wrong += wrong_selected

    total_score = total_correct - total_wrong
    success_percentage = (total_score / total_possible) * 100 if total_possible > 0 else 0

    conn = sqlite3.connect('quiz_results.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id TEXT,
        cin TEXT,
        first_name TEXT,
        last_name TEXT,
        correct INTEGER,
        wrong INTEGER,
        success_percentage REAL
    )
    ''')
    c.execute('''
    INSERT INTO results (emp_id, cin, first_name, last_name, correct, wrong, success_percentage)
    VALUES (?,?, ?, ?, ?, ?, ?)
    ''', (emp_id, cin, first_name, last_name, total_correct, total_wrong, success_percentage))

    conn.commit()
    conn.close()

    return render_template('merci.html')

@app.route('/graphs')
def graph():
    conn = sqlite3.connect('quiz_results.db')
    df = pd.read_sql_query("SELECT * from results", conn)
    conn.close()
    fig_individual = px.bar(df, x=df.index, y='success_percentage', title='Individual Success Percentage')
    fig_individual.update_layout(xaxis_title='Employee', yaxis_title='Success Percentage')

    avg_success_percentage = df['success_percentage'].mean()
    fig_all = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_success_percentage,
        title={'text': "Average Success Percentage"},
        gauge={'axis': {'range': [None, 100]}}
    ))
    individual_graph = fig_individual.to_html(full_html=False)
    all_graph = fig_all.to_html(full_html=False)
    pie_charts = {}
    for employee_id in df['emp_id'].unique():
        employee_data = df[df['emp_id'] == employee_id].iloc[0]
        labels = ['Correct', 'Wrong']
        values = [employee_data['correct'], employee_data['wrong']]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
        fig.update_layout(title_text=f'Employee {employee_id} Results')
        pie_charts[employee_id] = fig.to_html(full_html=False)
    return render_template('graphs.html', individual_graph=individual_graph, all_graph=all_graph,pie_charts=pie_charts)

@app.route('/export')
def export():
    conn = sqlite3.connect('quiz_results.db')
    df = pd.read_sql_query("SELECT * FROM results", conn)
    df.to_csv('results.csv', index=False)
    conn.close()
    return 'Results exported to results.csv'

@app.route('/view_results')
def view_results():
    conn = sqlite3.connect('quiz_results.db')
    c = conn.cursor()
    c.execute('SELECT * FROM results')
    rows = c.fetchall()
    conn.close()
    return render_template('view_results.html', results=rows)

if __name__ == '__main__':
    app.run(debug=True)