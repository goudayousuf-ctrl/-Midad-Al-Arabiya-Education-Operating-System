import os
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError(
        "متغير البيئة GEMINI_API_KEY غير موجود. "
        "أضفه من إعدادات مشروع Vercel (Settings -> Environment Variables) قبل التشغيل."
    )
client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_STYLE = (
    "تجنّب تماماً استخدام رموز النجوم أو الشباك في ردك. "
    "استخدم فقرات نصية واضحة وعناوين بارزة، وجداول منظمة عند الحاجة. "
    "التزم بالعربية الفصحى الدقيقة، ولا تخترع معلومة لغوية أو رقمية لا أساس لها."
)


def generate_with_fallback(prompt: str) -> str:
    max_retries = 3
    last_error = None
    for attempt in range(max_retries):
        try:
            chat = client.chats.create(model="gemini-2.0-flash")
            response = chat.send_message(prompt)
            if response and response.text:
                return response.text
            last_error = "استجابة فارغة من النموذج."
        except Exception as e:
            last_error = str(e)
            if attempt < max_retries - 1:
                time.sleep(1.5 * (attempt + 1))
    raise HTTPException(status_code=502, detail=f"تعذّر الحصول على رد من مداد بعد عدة محاولات: {last_error}")


# ===== نماذج البيانات =====
class AskRequest(BaseModel):
    query: str

class LessonRequest(BaseModel):
    topic: str

class AnalyzeRequest(BaseModel):
    class_name: str
    raw_notes: str

class CurriculumRequest(BaseModel):
    topic: str
    level: str

class BroadcastRequest(BaseModel):
    topic: str


# ===== نقاط النهاية =====
@app.post("/api/ask-madad")
def ask_madad(data: AskRequest):
    if not data.query or not data.query.strip():
        raise HTTPException(status_code=400, detail="السؤال فارغ.")
    prompt = (
        f"أنت 'مداد العربية AI'، المحرك الذكي المركزي لنظام تشغيل تعليمي يخدم معاهد تعليم العربية والقرآن. "
        f"أجب عن سؤال الإدارة أو المعلم التالي بدقة وعملية، مستندًا إلى أفضل الممارسات التربوية والإدارية "
        f"(حتى لو لم تُتَح لك بيانات المؤسسة الفعلية، اذكر بوضوح أن التحليل استرشادي عام وليس مبنيًا على أرقام حقيقية "
        f"ما لم يزودك السؤال بها). السؤال: {data.query}\n{SYSTEM_STYLE}"
    )
    return {"status": "success", "answer": generate_with_fallback(prompt)}


@app.post("/api/generate-lesson")
def generate_lesson(data: LessonRequest):
    if not data.topic or not data.topic.strip():
        raise HTTPException(status_code=400, detail="موضوع الدرس فارغ.")
    prompt = (
        f"أنت مساعد المعلم الذكي في 'مداد العربية AI'. جهّز خطة درس متكاملة بناءً على الطلب التالي: "
        f"{data.topic}\n"
        f"اشمل: الأهداف، التهيئة، عرض المحتوى، الأنشطة، ثم واجبًا تفاعليًا من 12 سؤالاً متدرج الصعوبة مع نموذج إجابة. "
        f"{SYSTEM_STYLE}"
    )
    return {"status": "success", "lesson_plan": generate_with_fallback(prompt)}


@app.post("/api/analyze-students")
def analyze_students(data: AnalyzeRequest):
    prompt = (
        f"أنت مستشار الإشراف التربوي الذكي في 'مداد العربية AI'. حلّل البيانات التالية عن الفصل أو المعلم "
        f"({data.class_name}) واستخرج الأنماط والتوصيات العلاجية العملية:\n"
        f"الملاحظات: {data.raw_notes or 'لا توجد ملاحظات مفصلة.'}\n"
        f"{SYSTEM_STYLE}"
    )
    return {"status": "success", "analysis_report": generate_with_fallback(prompt)}


@app.post("/api/financial-advisor")
def financial_advisor():
    prompt = (
        "أنت مستشار التطوير المالي والإداري في 'مداد العربية AI'. قدّم توصيات عامة لتحسين الكفاءة التشغيلية "
        "وزيادة الإيرادات لمعهد لتعليم العربية والقرآن، مع التنبيه بوضوح أن التوصيات استرشادية عامة ما لم تُزوَّد "
        f"بأرقام فعلية من المؤسسة.\n{SYSTEM_STYLE}"
    )
    return {"status": "success", "financial_report": generate_with_fallback(prompt)}


@app.post("/api/curriculum-plan")
def curriculum_plan(data: CurriculumRequest):
    if not data.topic or not data.topic.strip():
        raise HTTPException(status_code=400, detail="موضوع المنهج فارغ.")
    prompt = (
        f"أنت مساعد تصميم المناهج في 'مداد العربية AI'. صمم خطة منهج متكاملة حول: {data.topic}\n"
        f"المستوى الأكاديمي المستهدف: {data.level}\n"
        f"اشمل: عدد الوحدات المقترح، أهداف كل وحدة، المهارات اللغوية المستهدفة، وأفكار تقويم.\n"
        f"{SYSTEM_STYLE}"
    )
    return {"status": "success", "curriculum_plan": generate_with_fallback(prompt)}


@app.post("/api/broadcast-message")
def broadcast_message(data: BroadcastRequest):
    if not data.topic or not data.topic.strip():
        raise HTTPException(status_code=400, detail="موضوع الرسالة فارغ.")
    prompt = (
        f"أنت مساعد التواصل المؤسسي في 'مداد العربية AI'. اصغ رسالة تعميم احترافية ولطيفة حول: {data.topic}\n"
        f"قدّم نسختين: واحدة موجهة لأولياء الأمور/الطلاب، وأخرى موجهة لهيئة المعلمين.\n"
        f"{SYSTEM_STYLE}"
    )
    return {"status": "success", "broadcast": generate_with_fallback(prompt)}


@app.post("/api/executive-analytics")
def executive_analytics():
    prompt = (
        "أنت محلل البيانات التنفيذي الذكي في 'مداد العربية AI'. قدّم تحليلاً تشخيصياً عاماً لأداء مؤسسة تعليمية "
        "لتعليم العربية والقرآن (حضور، إنجاز واجبات، مخاطر انقطاع الطلاب)، مع توصيات عملية لرفع الكفاءة، "
        f"والتنبيه بوضوح أن التحليل استرشادي عام ما لم تُزوَّد ببيانات فعلية.\n{SYSTEM_STYLE}"
    )
    return {"status": "success", "executive_report": generate_with_fallback(prompt)}


@app.get("/api/health")
def health():
    return {"status": "ok"}
