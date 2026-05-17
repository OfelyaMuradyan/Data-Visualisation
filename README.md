# 🎬 Netflix Multi-Page Interactive Dashboard

Այս նախագիծը ինտերակտիվ Dashboard է, որը վերլուծում է Netflix-ի տվյալների բազան (Movies & TV Shows): Այն ստեղծված է **Python** լեզվով և **Plotly Dash** գրադարանի օգնությամբ։

## Հնարավորություններ
- **Overview Page**: Netflix-ի բովանդակության ընդհանուր վիճակագրություն։
- **Geography Page**: Ինտերակտիվ քարտեզ, որը ցույց է տալիս արտադրված բովանդակությունը ըստ երկրների։
- **Content Page**: Ժանրերի վերլուծություն և տևողության փոփոխությունը տարիների ընթացքում։
- **Multi-page Navigation**: Հարմարավետ sidebar մենյու էջերի միջև տեղաշարժվելու համար։

## Տեխնոլոգիաներ
- **Python**
- **Dash / Dash Bootstrap Components** (UI/UX)
- **Plotly** (Գրաֆիկների և քարտեզների համար)
- **Pandas** (Տվյալների մշակման համար)
- **Gunicorn** (Deployment-ի համար)

## 📁 Նախագծի Կառուցվածքը
```text
├── app.py              # Հիմնական ֆայլը (Entry point)
├── requirements.txt    # Անհրաժեշտ գրադարանների ցանկը
├── netflix_titles.csv  # Տվյալների բազան
├── pages/              # Էջերի թղթապանակը
│   ├── overview.py
│   ├── geography.py
│   └── content.py
└── README.md           # Նախագծի նկարագրությունը
