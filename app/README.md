# transcribe_api_demo
 
app/
├──- models/
│   ├── transcribe_model.py  # Hantering av olika transkriberingsmodeller
├── utils/
│   ├── pre_processor.py
├── main.py           # FastAPI huvudfil
├── requirements.txt      # Alla Python-beroenden
└── README.md             # Projektbeskrivning och instruktioner


### Usage
1. Install packages using `pip install -r requirements.txt`  
2. Run main file from the /app directory using `python -m uvicorn main:app --reload`
3. Test API by visiting [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Improvements
* Post processing using LLM
* Implementing multiple models
* Pre_processing class to be able to apply different pre proccesing effects depending on need. Also preprocess in the main file instead of transcribe.
* Credentials till en dotfile
* Google STT currently synchronous which needs to be fixed