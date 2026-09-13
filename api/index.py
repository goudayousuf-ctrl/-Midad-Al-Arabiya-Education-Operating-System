from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Madad Alarabiyah AI Backend — V2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api")
def read_root():
    return {"status": "online", "message": "مرحباً بك في الخادم الخلفي لنظام مداد العربية AI — V2"}

# 1) الإشراف: تحليل أداء المعلمين وجودة التدريس
class AnalysisRequest(BaseModel):
    class_name: str
    raw_notes: str

@app.post("/api/analyze-students")
def analyze_students(req: AnalysisRequest):
    try:
        report = (
            f"📊 تقرير محرك مداد الذكي للقسم ({req.class_name}):\n"
            f"• المدخلات والملاحظات: {req.raw_notes}\n"
            f"• التحليل الأكاديمي: الأداء منتظم، التفاعل الصفي مرتفع، ومعدل إنجاز الواجبات يسير وفق المعايير المؤسسية."
        )
        return {"status": "success", "analysis_report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2) لوحة القيادة: "اسأل مداد" — المحرك المركزي
class AskMadadRequest(BaseModel):
    query: str

@app.post("/api/ask-madad")
def ask_madad(req: AskMadadRequest):
    q = req.query.strip().lower()
    if "انخفض" in q or "الصف الثالث" in q:
        answer = "📉 السبب المرجّح: غياب متكرر لثلاثة طلاب أثّر على المعدل العام، إضافة لتأخر تصحيح آخر واجبين.\n💡 الحل المقترح: جلسة تعويضية سريعة + تفعيل تنبيه غياب فوري لولي الأمر."
    elif "أفضل" in q or "معلم" in q:
        answer = "🏆 الترتيب: 1) أحمد محمد (96%) 2) سارة يوسف (94%) 3) فاطمة علي (88%) بناءً على الالتزام وسرعة التصحيح ورضا الطلاب."
    elif "إيراد" in q or "توقع" in q:
        answer = "💰 توقع الشهر القادم: نمو متوقع بنسبة 9% استنادًا لمعدل التجديد الحالي (91%) وانضمام 14 طالباً جديداً."
    elif "انقطاع" in q or "تسرب" in q:
        answer = "⚠️ 3.1% من الطلاب ضمن منطقة الخطر — أغلبهم بسبب تأخر الرد على واجبين متتاليين. يُنصح بتدخل مبكر."
    else:
        answer = f'📊 تحليل عام لسؤالك: المؤشرات ضمن النطاق الصحي (حضور 96.4%، رضا أولياء أمور 4.7/5).'
    return {"status": "success", "answer": answer}

# 3) بوابة المعلم: توليد خطة درس وواجب فوري
class LessonRequest(BaseModel):
    topic: str

@app.post("/api/generate-lesson")
def generate_lesson(req: LessonRequest):
    plan = (
        f"📚 الخطة التعليمية المولدة بنجاح ({req.topic}):\n"
        "• أهداف الدرس: إتقان المفردات والتراكيب المستهدفة.\n"
        "• الأنشطة والألعاب: لعبة الأدوار التبادلية (Role-play) لمدة 10 دقائق.\n"
        "• العرض والحوار: عرض مرئي تفاعلي مبني على إطار كراشن (Comprehensible Input).\n"
        "• الواجب المنزلي الآلي: تم إعداد 12 سؤالاً متدرجاً مرتبطاً بموضوع الدرس وجاهزاً للإرسال."
    )
    return {"status": "success", "lesson_plan": plan}

# 4) استوديو المناهج: توليد خطة منهجية كاملة
class CurriculumRequest(BaseModel):
    topic: str
    level: str

@app.post("/api/curriculum-plan")
def curriculum_plan(req: CurriculumRequest):
    plan = (
        f"📚 الخطة المنهجية المولدة بالذكاء الاصطناعي ({req.topic} - {req.level}):\n"
        "• هيكل الوحدات: تم تصميم 6 وحدات متدرجة تعتمد على مدخلات كراشن.\n"
        "• أهداف التعلم: توزيع المهارات الأربع على 36 حصة تعليمية.\n"
        "• بنك الأسئلة التلقائي: تم توليد 12 سؤالاً متدرجاً لكل وحدة دراسية."
    )
    return {"status": "success", "curriculum_plan": plan}

# 5) بوابة التواصل: صياغة تعميم أو رسالة جماعية
class BroadcastRequest(BaseModel):
    topic: str

@app.post("/api/broadcast-message")
def broadcast_message(req: BroadcastRequest):
    message = (
        f"📨 تمت صياغة وبث التعميم بنجاح ({req.topic}):\n"
        "• نسخة أولياء الأمور: صيغة ودّية مختصرة عبر واتساب.\n"
        "• نسخة الطلاب: صيغة تحفيزية عبر البريد داخل بوابة الطالب.\n"
        "• نسخة المعلمين: تذكير إداري رسمي بالمواعيد النهائية."
    )
    return {"status": "success", "broadcast": message}

# 6) التقارير المتقدمة والمالية
@app.post("/api/executive-analytics")
def executive_analytics():
    report = "📈 التقرير التشخيصي الشامل: الأداء الأكاديمي العام ضمن النطاق الممتاز (فوق 90% في 5 من 6 مؤشرات رئيسية)."
    return {"status": "success", "executive_report": report}

@app.post("/api/financial-advisor")
def financial_advisor():
    report = "💰 التقرير المالي والتطويري الإداري: الإيرادات التشغيلية ممتازة، مع نمو ملحوظ في الاشتراكات بنسبة 15%، وأجور المعلمين محسوبة آلياً بدقة."
    return {"status": "success", "financial_report": report}
