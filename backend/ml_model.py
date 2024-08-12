from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
import pandas as pd
import warnings
import joblib
data = {
    'Deficiency': ['Protein-energy', 'Iron', 'Magnesium', 'Potassium', 'Vitamins B1, B12, B3',
                   'Vitamin C', 'Zinc', 'Folate', 'Vitamin D', 'Vitamin B2 – riboflavin',
                   'Vitamin A', 'Vitamin B6', 'Essential Fatty Acids', 'Iodine', 'Calcium', 'Biotin'],
    'Symptoms': [
        'Fatigue, Muscle wasting, Weight loss, Swelling of legs, Delayed wound healing, Frequent infection3s, Loss of appetite, Pale skin, Weakness, Dizziness',
        'Fatigue, Loss of appetite, Cold intolerance, Pale appearance due to anaemia, Itchy skin, Sore tongue, Scalp hair loss, Brittle or flaking nails, Calf muscle pain after minimal exercise, Shortness of breath, Weakness, Dizziness, Chest pain, Rapid heartbeat',
        'Fatigue, Muscle pains and cramps, Calf muscle pain after minimal exercise, Nausea, Vomiting, Tremors, Seizures, Irregular heartbeat, High blood pressure, Anxiety',
        'Fatigue, Palpitations, Muscle weakness, Irregular heartbeat, Nausea, Vomiting, Diarrhea, Abdominal cramping, Constipation, Muscle cramps, Tingling or numbness',
        'Fatigue, Loss of appetite, Loss of taste, Muscle wasting, Sore tongue, Recurrent mouth ulcers, Dry skin, Mood changes, Confusion, Memory loss, Numbness or tingling in hands and feet, Muscle weakness, Difficulty walking, Anemia, Diarrhea',
        'Fatigue, Pica eating non-nutritive substances, Excessive bruising, Haemorrhage or redness around hair follicles, Plugging of hair follicles with keratin or coiled hairs, Enlarged veins under the tongue with micro-haemorrhages, Twitching of facial muscles when tapping on the facial nerve in front of the ear, Bleeding gums, Weak immune system, Scurvy, Swollen joints, Easy bruising, Nosebleeds',
        'Loss of appetite, Pica eating non-nutritive substances, Loss of taste, Carotenoderma – yellow discolouration of the skin, Redness at the sides of the nose, Spoon-shaped nails, Impaired wound healing, Hair loss, Poor growth in children, Delayed wound healing, Impaired immune function, Mental lethargy',
        'Pale appearance due to anaemia, Cracking at the corners of the mouth, Recurrent mouth ulcers, Restless legs, Poor concentration, Peripheral neuropathy – numbness, tingling, disordered sensation, pain, and/or weakness in the hands or feet, Depression, Mental confusion, Weakness, Bone pain, Osteoporosis, Fractures, Muscle cramps, Irregular heartbeat',
        'Carotenoderma – yellow discolouration of the skin, Loss of height and excessive curvature of the spine, Bowed legs, Muscle pains and cramps, Walking with a waddling gait, Difficulty getting up from a low chair or climbing the stairs or weakness of shoulder muscles, Loss of balance when standing upright with feet together and the eyes closed, Loss of vibration sensation in the lower limbs, Unsteady movement or walking, Heart failure, Bone pain, Fractures, Muscle weakness, Fatigue, Depression',
        'Cracking and peeling of skin on the lips, Redness at the sides of the nose, Redness or cracking at the outer angle of the eyes, Burning feet syndrome, Sore throat, Swelling and soreness of the mouth and throat, Skin rash, Hair loss, Depression, Fatigue, Hallucinations, Muscle pain, Numbness or tingling in hands and feet',
        'Poor night vision, Conjunctival dryness, Dry eyes, Night blindness, Corneal ulcers, Sensitivity to light, Skin rash, Dry skin, Vision problems, Dry eyes, Night blindness, Dry hair, Dry skin, Throat irritation',
        'Redness at the sides of the nose, Fatigue, Irritability, Confusion, Muscle pain, Seizures, Skin rash, Depression, Memory loss, Anemia, Mouth sores, Weak immune system, Abnormal heart rhythms',
        'Dry skin, Nails - brittle or flaking, Poor wound healing, Dandruff, Dry eyes, Cracked lips, Dry mouth, Skin rash, Depression, Irritability, Confusion, Fatigue, Weakness, Headache, Nausea, Constipation',
        'Goitre, Dry and scaly skin, Brittle hair and nails, Depression, Difficulty concentrating, Weight gain, Sensitivity to cold, Fatigue, Muscle weakness, Joint pain, Cramps, Nausea, Loss of appetite',
        'Loss of height and excessive curvature of the spine, Muscle pains and cramps, Excessive calf muscle tenderness, Walking with a waddling gait, Difficulty getting up from a low chair or climbing the stairs or weakness of shoulder muscles, Bowed legs, Bone pain, Osteoporosis, Kidney stones, Muscle weakness, Fatigue, Joint pain, Memory loss, Constipation, Nausea, Vomiting',
        'Poor concentration, Depression, Dry and scaly skin, Brittle hair and nails, Hair loss, Weak immune system, Difficulty sleeping, Mood swings, Fatigue, Nausea, Vomiting, Loss of appetite, Muscle cramps, Numbness or tingling in hands and feet'
    ]
}


sample_df = pd.DataFrame(data)
symptom_list = []
deficiency_list = []

for index, row in sample_df.iterrows():
    symptoms = row['Symptoms'].split(', ')
    for symptom in symptoms:
        symptom_list.append(symptom)
        deficiency_list.append(row['Deficiency'])


df = pd.DataFrame({'Symptom': symptom_list, 'Deficiency': deficiency_list})



df['combined_text'] = df['Symptom']+' '+df['Deficiency']


label_mapping = dict(enumerate(df['Deficiency'].astype('category').cat.categories))
df['Label'] = df['Deficiency'].astype('category').cat.codes


X_train, X_test, y_train, y_test = train_test_split(df['combined_text'], df['Label'], test_size=0.2, random_state=42)


tfidf_vectorizer = TfidfVectorizer()
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)



model_rf = RandomForestClassifier(n_estimators=100, random_state=42)
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    cross_val_scores = cross_val_score(model_rf, X_train_tfidf, y_train, cv=5)
average_accuracy = cross_val_scores.mean()
print(f'Average Cross-Validation Accuracy: {average_accuracy}')


model_rf.fit(X_train_tfidf, y_train)
y_pred_rf = model_rf.predict(X_test_tfidf)
accuracy_rf = accuracy_score(y_test, y_pred_rf)
print(f'Test Accuracy: {accuracy_rf}')

joblib.dump(model_rf, 'model_rf.pkl')
joblib.dump(tfidf_vectorizer, 'tfidf_vectorizer.pkl')