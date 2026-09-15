import os
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

app = FastAPI(title="Madad Alarabiyah AI Engine — Core")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("متغير البيئة GEMINI_API_KEY غير موجود في إعدادات Vercel.")

client = genai.Client(api_key=GEMINI_API_KEY)

# =====================================================================
# دستور مداد المعرفي (قواعد الخبير التربوي والمشرف والباحث الشرعي)
# =====================================================================
MADAD_CORE_INSTRUCTION = (
    "أنت 'مداد العربية AI'، المحرك المعرفي والتشغيلي المركزي لمؤسسات تعليم اللغة العربية، "
    "القرآن الكريم، والعلوم الشرعية. شخصيتك ومنهجيتك تدمج بين:\n"
    "1. الخبير التربوي ومصمم المناهج: تستند لنظريات اكتساب اللغة الحديثة (مثل المدخلات المفهومة Comprehensible Input، "
    "ومنهجية التعلّم القصصي التفاعلي TPRS، والتدرج وفق المعايير الدولية كالإطار الأوروبي CEFR).\n"
    "2. المشرف التعليمي الحصيف: تُحلل المشكلات الأكاديمية بنظرة تشخيصية تبحث في الأسباب الجذرية لا المظاهر، "
    "وتطرح حلولاً علاجية وتطويرية إجرائية وقابلة للقياس الميداني.\n"
    "3. الباحث العلمي والشرعي الرصين: تتحرى الأمانة العلمية والدقة البالغة في أحكام التجويد والعلوم الشرعية والمصطلحات، "
    "وتقدم مادة موثقة ورصينة بعيدة عن التسطيح أو التكلف.\n"
    "4. الضوابط الأسلوبية: تحدّث بعربية فصحى بيانية راقية وجزلة. تجنّب تماماً رموز النجوم (*) أو الشباك (#) في التنسيق، "
    "واعتمد على العناوين الواضحة، والفقرات المترابطة، والجداول التنسيقية المنظمة عند المقارنة أو عرض الخطط."
)


def generate_with_madad_rules(specific_prompt: str) -> str:
    full_prompt = f"{MADAD_CORE_INSTRUCTION}\n\nالمهمة المطلوبة:\n{specific_prompt}"
    max_retries = 3
    last_error = None
    for attempt in range(max_retries):
        try:
            # استخدام الطريقة المباشرة والأحدث مع النموذج المتاح حالياً
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=full_prompt,
            )
            if response and response.text:
                return response.text
            last_error = "استجابة فارغة من المحرك المعرفي."
        except Exception as e:
            last_error = str(e)
            if attempt < max_retries - 1:
                time.sleep(1.5 * (attempt + 1))
    raise HTTPException(status_code=502, detail=f"تعذر استدعاء محرك مداد: {last_error}")


# ===== نماذج البيانات المدخلة =====
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


# ===== نقاط النهاية المفعلة والمشروطة بقواعد مداد =====

@app.post("/api/ask-madad")
def ask_madad(data: AskRequest):
    if not data.query or not data.query.strip():
        raise HTTPException(status_code=400, detail="السؤال أو الاستشارة فارغة.")
    prompt = (
        f"بصفتك المستشار التربوي والتنفيذي الأعلى للمؤسسة، أجب عن استشارة الإدارة أو المعلم التالية:\n"
        f"الاستفسار: {data.query}\n"
        f"قدّم تحليلاً تشخيصياً لواقع الحالة، يتبعه حلول إجرائية مرتبة وقابلة للتطبيق الفوري في البيئة التعليمية."
    )
    return {"status": "success", "answer": generate_with_madad_rules(prompt)}


@app.post("/api/generate-lesson")
def generate_lesson(data: LessonRequest):
    if not data.topic or not data.topic.strip():
        raise HTTPException(status_code=400, detail="موضوع الدرس فارغ.")
    prompt = (
        f"قم بإعداد خطة درس نموذجية متكاملة حول موضوع: ({data.topic}).\n"
        f"التزم بالهيكل التالي:\n"
        f"1. الأهداف الإجرائية (معرفية، مهارية، وجدانية).\n"
        f"2. التهيئة الحافزة وتقديم المفردات الجديدة عبر السياق الطبيعي (Comprehensible Input).\n"
        f"3. النشاط التفاعلي الرئيس (تطبيق عملي أو تمثيل أدوار TPRS).\n"
        f"4. تقويم ختامي وتطبيق منزلي يتضمن بنك أسئلة متدرج من 12 فقرة مع مفتاح التصحيح."
    )
    return {"status": "success", "lesson_plan": generate_with_madad_rules(prompt)}


@app.post("/api/analyze-students")
def analyze_students(data: AnalyzeRequest):
    prompt = (
        f"بصفتك خبيراً في الإشراف التربوي وضمان الجودة، حلّل التقرير والملاحظات الميدانية لقسم: ({data.class_name}).\n"
        f"الملاحظات المرصودة:\n{data.raw_notes or 'ملاحظات عامة حول الانتظام والتفاعل'}\n"
        f"المطلوب: استخراج مؤشرات القوة، نقاط الفجوة الأكاديمية أو السلوكية، ثم صياغة خطة دعم وتغذية راجعة موجهة للمعلم."
    )
    return {"status": "success", "analysis_report": generate_with_madad_rules(prompt)}


@app.post("/api/curriculum-plan")
def curriculum_plan(data: CurriculumRequest):
    if not data.topic or not data.topic.strip():
        raise HTTPException(status_code=400, detail="موضوع المنهج فارغ.")
    prompt = (
        f"بصفتك خبير بناء وتطوير مناهج تعليم العربية والعلوم المرتبطة بها:\n"
        f"صمم خارطة منهجية للموضوع: ({data.topic}) والمستوى المستهدف: ({data.level}).\n"
        f"فصّل الخطة إلى وحدات تعليمية، مع توزيع المهارات الأربع (الاستماع، التحدث، القراءة، الكتابة)، "
        f"وتحديد الكفايات اللغوية والشرعية المتوقع إتقانها بنهاية المنهج."
    )
    return {"status": "success", "curriculum_plan": generate_with_madad_rules(prompt)}


@app.post("/api/broadcast-message")
def broadcast_message(data: BroadcastRequest):
    if not data.topic or not data.topic.strip():
        raise HTTPException(status_code=400, detail="موضوع التعميم فارغ.")
    prompt = (
        f"صِغ تعميماً مؤسسياً مهنياً وبلاغياً رفيعاً حول: ({data.topic}).\n"
        f"وفّر نسختين:\n"
        f"- الأولى: موجهة لأولياء الأمور والطلاب بأسلوب تربوي لطيف ومحفز.\n"
        f"- الثانية: موجهة للهيئة التعليمية والإدارية بصيغة إدارية تنظيمية دقيقة."
    )
    return {"status": "success", "broadcast": generate_with_madad_rules(prompt)}


@app.post("/api/financial-advisor")
def financial_advisor():
    prompt = (
        "قدّم رؤية استشارية متكاملة لمدير معهد تعليمي لتحقيق التوازن بين الاستدامة المالية "
        "وتحفيز الكادر التعليمي، مع نماذج مقترحة لمكافآت الأداء المرتبطة بجودة المخرجات التربوية."
    )
    return {"status": "success", "financial_report": generate_with_madad_rules(prompt)}


@app.post("/api/executive-analytics")
def executive_analytics():
    prompt = (
        "قدّم تحليلاً تنفيذياً شاملاً لواقع العمل في مؤسسة تعليمية (حضور الطلاب، كفاءة التصحيح، "
        "معدلات استبقاء الطلاب والحد من التسرب)، مع مصفوفة توصيات إدارية وتربوية للفترة القادمة."
    )
    return {"status": "success", "executive_report": generate_with_madad_rules(prompt)}


@app.get("/api/health")
def health():
    return {"status": "ok", "system": "Madad Engine Active"}
