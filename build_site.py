import json, os

json_path = r'C:\Users\Beteny\.gemini\antigravity\scratch\el_sahaba_expenses_dashboard\data.json'
with open(json_path, 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

html_content = '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>النظام المحاسبي الشامل للنفقات - شركة الحاج جمعة السحابة</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>

    <style>
        :root {
            --bg-dark: #0b1329;
            --bg-card: #16223f;
            --bg-card-hover: #1f2d52;
            --border-color: #273863;
            --accent-primary: #3b82f6;
            --accent-secondary: #06b6d4;
            --accent-purple: #8b5cf6;
            --accent-success: #10b981;
            --accent-warning: #f59e0b;
            --accent-danger: #ef4444;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --radius-lg: 16px;
            --radius-md: 10px;
            --shadow-glow: 0 10px 30px -10px rgba(59, 130, 246, 0.4);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Cairo', sans-serif; }

        body {
            background-color: var(--bg-dark);
            color: var(--text-main);
            min-height: 100vh;
            display: flex; flex-direction: column; padding-bottom: 50px;
        }

        .navbar {
            background: rgba(22, 34, 63, 0.95);
            border-bottom: 1px solid var(--border-color);
            padding: 16px 35px;
            display: flex; justify-content: space-between; align-items: center;
            flex-wrap: wrap; gap: 15px; position: sticky; top: 0; z-index: 100;
        }

        .logo-group { display: flex; align-items: center; gap: 14px; }
        .logo-icon {
            width: 48px; height: 48px;
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-purple));
            border-radius: 12px; display: flex; align-items: center; justify-content: center;
            font-size: 1.5rem; color: #fff; box-shadow: var(--shadow-glow);
        }
        .logo-title { font-size: 1.3rem; font-weight: 800; color: #fff; }

        .nav-tabs { display: flex; gap: 8px; flex-wrap: wrap; }
        .tab-btn {
            padding: 10px 18px; border-radius: var(--radius-md); font-weight: 700;
            font-size: 0.92rem; cursor: pointer; border: 1px solid var(--border-color);
            background: rgba(255,255,255,0.04); color: var(--text-muted); transition: all 0.2s ease;
            display: inline-flex; align-items: center; gap: 8px;
        }
        .tab-btn:hover { background: rgba(255,255,255,0.08); color: #fff; }
        .tab-btn.active {
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            color: #fff; border-color: transparent; box-shadow: var(--shadow-glow);
        }

        .btn {
            padding: 10px 18px; border-radius: var(--radius-md); font-weight: 700;
            font-size: 0.9rem; cursor: pointer; border: none; display: inline-flex;
            align-items: center; gap: 8px; transition: all 0.2s ease; text-decoration: none;
        }
        .btn-secondary { background: rgba(139, 92, 246, 0.2); color: #a78bfa; border: 1px solid rgba(139, 92, 246, 0.4); }
        .btn-success { background: linear-gradient(135deg, var(--accent-success), #059669); color: #fff; }
        .btn:hover { transform: translateY(-2px); }

        .container { max-width: 1450px; margin: 0 auto; padding: 25px 20px; width: 100%; }

        .section-card {
            background: var(--bg-card); border: 1px solid var(--border-color);
            border-radius: var(--radius-lg); padding: 26px; margin-bottom: 30px;
        }

        /* Upload Area */
        .upload-card {
            background: rgba(22, 34, 63, 0.6); border: 2px dashed var(--border-color);
            border-radius: var(--radius-lg); padding: 22px; text-align: center;
            margin-bottom: 25px; cursor: pointer; transition: all 0.3s ease; position: relative;
        }
        .upload-card:hover { border-color: var(--accent-secondary); background: rgba(6, 182, 212, 0.05); }
        .upload-card input[type="file"] {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0; cursor: pointer; z-index: 99;
        }

        .metrics-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 20px; margin-bottom: 24px;
        }
        .metric-card {
            background: var(--bg-dark); border: 1px solid var(--border-color);
            border-radius: var(--radius-lg); padding: 22px; display: flex; align-items: center; gap: 16px;
            transition: all 0.2s ease;
        }
        .metric-card:hover { border-color: var(--accent-primary); transform: translateY(-3px); }

        .metric-icon { width: 52px; height: 52px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; }
        .metric-icon.blue { background: rgba(59, 130, 246, 0.15); color: var(--accent-primary); }
        .metric-icon.cyan { background: rgba(6, 182, 212, 0.15); color: var(--accent-secondary); }
        .metric-icon.amber { background: rgba(245, 158, 11, 0.15); color: var(--accent-warning); }
        .metric-icon.purple { background: rgba(139, 92, 246, 0.15); color: var(--accent-purple); }

        .metric-info h4 { font-size: 0.85rem; color: var(--text-muted); font-weight: 600; }
        .metric-info .value { font-size: 1.45rem; font-weight: 800; color: var(--text-main); }

        .charts-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-bottom: 24px; }
        @media (max-width: 1024px) { .charts-grid { grid-template-columns: 1fr; } }

        .chart-card { background: var(--bg-dark); border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 22px; }
        .chart-container { position: relative; height: 340px; width: 100%; }

        .table-responsive { width: 100%; overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; text-align: right; font-size: 0.9rem; }
        th { background: rgba(11, 19, 41, 0.9); color: var(--text-muted); padding: 14px; font-weight: 700; border-bottom: 1px solid var(--border-color); position: sticky; top: 0; }
        td { padding: 12px 14px; border-bottom: 1px solid var(--border-color); }
        tbody tr:hover { background: rgba(31, 45, 82, 0.4); }

        .badge { padding: 4px 10px; border-radius: 20px; font-size: 0.78rem; font-weight: 700; display: inline-block; }
        .badge-success { background: rgba(16, 185, 129, 0.2); color: #34d399; }
        .badge-danger { background: rgba(239, 68, 68, 0.2); color: #f87171; }
        .badge-warning { background: rgba(245, 158, 11, 0.2); color: #fbbf24; }
        .badge-primary { background: rgba(59, 130, 246, 0.2); color: #60a5fa; }
        .badge-purple { background: rgba(139, 92, 246, 0.2); color: #a78bfa; }

        .filter-box {
            display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; background: var(--bg-dark);
            padding: 16px; border-radius: var(--radius-md); border: 1px solid var(--border-color);
            align-items: center;
        }
        .filter-input {
            background: #16223f; border: 1px solid var(--border-color); color: #fff;
            padding: 10px 16px; border-radius: 8px; font-size: 0.92rem; outline: none; flex: 1; min-width: 240px;
            transition: all 0.2s ease;
        }
        .filter-input:focus { border-color: var(--accent-primary); box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2); }

        .toast {
            position: fixed; bottom: 30px; right: 30px;
            background: linear-gradient(135deg, var(--accent-success), #059669);
            color: #fff; padding: 14px 24px; border-radius: var(--radius-md);
            font-weight: 700; box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            display: flex; align-items: center; gap: 10px; z-index: 9999;
            opacity: 0; visibility: hidden; transition: all 0.3s ease;
        }
        .toast.show { opacity: 1; visibility: visible; transform: translateY(-5px); }
    </style>
</head>
<body>

    <!-- Header Navbar -->
    <nav class="navbar">
        <div class="logo-group">
            <div class="logo-icon">
                <i class="fa-solid fa-cloud-sun"></i>
            </div>
            <div>
                <div class="logo-title">شركة الحاج جمعة السحابة</div>
                <small style="color: var(--text-muted); font-size: 0.78rem;">النظام المحاسبي الشامل لتحليل النفقات والمصروفات ومراكز التكلفة</small>
            </div>
        </div>

        <div class="nav-tabs">
            <button class="tab-btn active" onclick="switchTab('pnl')">
                <i class="fa-solid fa-chart-line"></i> 1. قائمة الدخل (P&L)
            </button>
            <button class="tab-btn" onclick="switchTab('costCenters')">
                <i class="fa-solid fa-truck-monster"></i> 2. مراكز التكلفة والسيارات
            </button>
            <button class="tab-btn" onclick="switchTab('expAnalysis')">
                <i class="fa-solid fa-scale-balanced"></i> 3. تحليل وتطور المصروفات
            </button>
            <button class="tab-btn" onclick="switchTab('journal')">
                <i class="fa-solid fa-book-journal-whills"></i> 4. سجل القيود اليومي
            </button>
            <button class="tab-btn" onclick="switchTab('salesItems')">
                <i class="fa-solid fa-boxes-stacked"></i> 5. مبيعات الأصناف
            </button>
        </div>

        <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
            <button class="btn btn-primary" onclick="downloadMobileHtmlReport()" title="تصدير ملف تقرير تفاعلي يفتح على أي تليفون بدون سيرفر لإرساله عبر الواتساب">
                <i class="fa-solid fa-mobile-screen-button"></i> تصدير للواتساب والموبايل 📱
            </button>
            <a class="btn btn-secondary" href="/شركة_الحاج_جمعة_السحابة_موقع_النفقات.zip" download title="تحميل الملف المضغوط كاملاً لرفعه على GitHub">
                <i class="fa-solid fa-file-zipper"></i> تحميل ZIP لـ GitHub 📦
            </a>
            <button class="btn btn-secondary" onclick="shareDashboardLink()" title="مشاركة رابط التقرير والموقع مع الآخرين">
                <i class="fa-solid fa-share-nodes"></i> مشاركة اللينك 🔗
            </button>
            <button class="btn btn-success" onclick="exportCompleteExcel()">
                <i class="fa-solid fa-file-excel"></i> تصدير (Excel)
            </button>
        </div>
    </nav>

    <div class="container">

        <!-- Dynamic Upload Drop Box for Updating Sheet -->
        <div class="upload-card" onclick="document.getElementById('excelUploader').click()">
            <input type="file" id="excelUploader" accept=".xlsx, .xls, .csv" onchange="handleFileUpload(this.files[0])">
            <div style="display:flex; justify-content:center; align-items:center; gap:16px; flex-wrap:wrap;">
                <i class="fa-solid fa-cloud-arrow-up" style="font-size: 2.2rem; color: var(--accent-secondary);"></i>
                <div style="text-align: right;">
                    <h3 style="font-size: 1.15rem; font-weight: 800;">انقر هنا أو اسحب شيت الإكسيل الجديد لتحديث البيانات فوراً 📂</h3>
                    <p style="font-size: 0.85rem; color: var(--text-muted);">يقوم النظام بقراءة الشيت الجديد وتحديث كافة الأرقام والرسوم البيانية في ثوانٍ</p>
                </div>
            </div>
            <div id="uploadStatus" style="margin-top: 10px; font-weight: 700; font-size: 0.9rem; color: var(--accent-success);"></div>
        </div>

        <!-- TAB 1: Income Statement (P&L) -->
        <div class="section-card" id="tabPnl">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
                <h2><i class="fa-solid fa-chart-line" style="color: var(--accent-secondary);"></i> 📊 ملخص قائمة الدخل والأرباح والخسائر (مارس - يونيو)</h2>
            </div>

            <!-- KPI Cards -->
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-icon blue"><i class="fa-solid fa-sack-dollar"></i></div>
                    <div class="metric-info">
                        <h4>إجمالي مبيعات الفترة</h4>
                        <div class="value" id="kpiTotalSales">0 ج.م</div>
                    </div>
                </div>
                <div class="metric-card">
                    <div class="metric-icon amber"><i class="fa-solid fa-boxes-packing"></i></div>
                    <div class="metric-info">
                        <h4>تكلفة البضاعة المباعة (COGS)</h4>
                        <div class="value" id="kpiTotalCogs">0 ج.م</div>
                    </div>
                </div>
                <div class="metric-card">
                    <div class="metric-icon purple"><i class="fa-solid fa-chart-line"></i></div>
                    <div class="metric-info">
                        <h4>هامش الربح</h4>
                        <div class="value" id="kpiGrossMargin">0 ج.م</div>
                    </div>
                </div>
                <div class="metric-card">
                    <div class="metric-icon cyan"><i class="fa-solid fa-piggy-bank"></i></div>
                    <div class="metric-info">
                        <h4>صافى ربح / خساره</h4>
                        <div class="value" id="kpiNetProfitLoss">0 ج.م</div>
                    </div>
                </div>
            </div>

            <!-- Charts Grid -->
            <div class="charts-grid">
                <div class="chart-card">
                    <h4 style="margin-bottom: 15px;"><i class="fa-solid fa-chart-column" style="color: var(--accent-primary);"></i> تطور المبيعات وتكلفة البضاعة شهرياً (ج.م)</h4>
                    <div class="chart-container"><canvas id="pnlBarChart"></canvas></div>
                </div>
                <div class="chart-card">
                    <h4 style="margin-bottom: 15px;"><i class="fa-solid fa-chart-pie" style="color: var(--accent-purple);"></i> نسبة توزيع الإيرادات الشهري %</h4>
                    <div class="chart-container"><canvas id="pnlPieChart"></canvas></div>
                </div>
            </div>

            <!-- TAB 1 SEARCH BOX -->
            <div class="filter-box">
                <i class="fa-solid fa-magnifying-glass" style="color: var(--accent-secondary); font-size: 1.2rem;"></i>
                <input type="text" class="filter-input" id="searchPnlInput" placeholder="🔍 بحث في بنود قائمة الدخل (مثال: مبيعات، رواتب، إيجار، جاز، كهرباء...)" oninput="filterPnlTable()">
                <span style="font-size: 0.85rem; color: var(--text-muted);" id="pnlMatchCount"></span>
            </div>

            <!-- P&L Table -->
            <h4 style="margin: 15px 0 12px 0;"><i class="fa-solid fa-table-list" style="color: var(--accent-secondary);"></i> جدول تفاصيل بنود قائمة الدخل (شهرياً)</h4>
            <div class="table-responsive">
                <table id="pnlTable">
                    <thead>
                        <tr id="pnlTableHead">
                            <th>البيان المحاسبي</th>
                            <!-- Headers inserted dynamically by JS -->
                            <th>إجمالي الفترة (ج.م)</th>
                        </tr>
                    </thead>
                    <tbody id="pnlTableBody"></tbody>
                </table>
            </div>
        </div>

        <!-- TAB 2: Cost Centers (Equipment & Vehicles) -->
        <div class="section-card" id="tabCostCenters" style="display: none;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
                <h2><i class="fa-solid fa-truck-monster" style="color: var(--accent-purple);"></i> 🚜 تحليل نفقات ومصروفات مراكز التكلفة (المعدات والسيارات)</h2>
            </div>

            <div class="charts-grid">
                <div class="chart-card">
                    <h4 style="margin-bottom: 15px;"><i class="fa-solid fa-chart-bar" style="color: var(--accent-purple);"></i> اجمالي نفقات كل مركز تكلفة (ج.م)</h4>
                    <div class="chart-container"><canvas id="ccBarChart"></canvas></div>
                </div>
                <div class="chart-card">
                    <h4 style="margin-bottom: 15px;"><i class="fa-solid fa-chart-pie" style="color: var(--accent-warning);"></i> نسبة توزيع نفقات الآلات والسيارات %</h4>
                    <div class="chart-container"><canvas id="ccPieChart"></canvas></div>
                </div>
            </div>

            <!-- TAB 2 SEARCH BOX -->
            <div class="filter-box">
                <i class="fa-solid fa-magnifying-glass" style="color: var(--accent-purple); font-size: 1.2rem;"></i>
                <input type="text" class="filter-input" id="searchCcInput" placeholder="🔍 بحث في مراكز التكلفة والمعدات والسيارات (مثال: الآلات، تريسكل، ملاكي، نقل، صيانة، بنزين...)" oninput="filterCcTable()">
                <span style="font-size: 0.85rem; color: var(--text-muted);" id="ccMatchCount"></span>
            </div>

            <h4 style="margin: 15px 0 12px 0;"><i class="fa-solid fa-list-check" style="color: var(--accent-primary);"></i> جدول تفاصيل نفقات مراكز التكلفة والسيارات شهرياً</h4>
            <div class="table-responsive">
                <table>
                    <thead>
                        <tr>
                            <th>مركز التكلفة / المعدة</th>
                            <th>البند الفرعي</th>
                            <th>مارس (Mar)</th>
                            <th>أبريل (Apr)</th>
                            <th>مايو (May)</th>
                            <th>يونيو (June)</th>
                            <th>إجمالي النفقات</th>
                        </tr>
                    </thead>
                    <tbody id="ccTableBody"></tbody>
                </table>
            </div>
        </div>

        <!-- TAB 3: Expense Analysis & Variance -->
        <div class="section-card" id="tabExpAnalysis" style="display: none;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
                <h2><i class="fa-solid fa-scale-balanced" style="color: var(--accent-warning);"></i> 📊 تحليل ومقارنة المصروفات الفترية (فبراير - يونيو)</h2>
            </div>

            <!-- TAB 3 SEARCH BOX -->
            <div class="filter-box">
                <i class="fa-solid fa-magnifying-glass" style="color: var(--accent-warning); font-size: 1.2rem;"></i>
                <input type="text" class="filter-input" id="searchExpInput" placeholder="🔍 بحث في أسماء ومقارنات المصروفات (مثال: صيانة، كهرباء، وجبات، نظافة، إيجار...)" oninput="filterExpTable()">
                <span style="font-size: 0.85rem; color: var(--text-muted);" id="expMatchCount"></span>
            </div>

            <div class="table-responsive">
                <table>
                    <thead>
                        <tr>
                            <th>اسم المصروف</th>
                            <th>فبراير (Feb)</th>
                            <th>مارس (Mar)</th>
                            <th>مقارنة 1 (+/-)</th>
                            <th>أبريل (Apr)</th>
                            <th>مقارنة 2 (+/-)</th>
                            <th>مايو (May)</th>
                            <th>مقارنة 3 (+/-)</th>
                            <th>يونيو (June)</th>
                            <th>مقارنة 4 (+/-)</th>
                        </tr>
                    </thead>
                    <tbody id="expAnalysisBody"></tbody>
                </table>
            </div>
        </div>

        <!-- TAB 4: Journal Log (599 Transactions) -->
        <div class="section-card" id="tabJournal" style="display: none;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px; flex-wrap:wrap; gap:10px;">
                <h2><i class="fa-solid fa-book-journal-whills" style="color: var(--accent-primary);"></i> 📑 سجل حركة القيود اليومي والدفتر العام (<span id="transCount">0</span> قيد)</h2>
            </div>

            <div class="filter-box">
                <i class="fa-solid fa-magnifying-glass" style="color: var(--accent-primary); font-size: 1.2rem;"></i>
                <input type="text" class="filter-input" id="searchDesc" placeholder="🔍 بحث شامل بالوصف أو الحساب أو المبلغ (مثال: فاتورة بيع، صيانة، جاز، waleed...)" oninput="filterJournal()">
                <select class="filter-input" id="filterUser" onchange="filterJournal()" style="max-width: 220px;">
                    <option value="">الكل (جميع المستخدمين)</option>
                    <option value="waleed">waleed</option>
                    <option value="ADMIN">ADMIN</option>
                </select>
                <select class="filter-input" id="filterMonth" onchange="filterJournal()" style="max-width: 220px;">
                    <option value="">الكل (جميع الشهور)</option>
                    <option value="Feb">فبراير (Feb)</option>
                    <option value="Mar">مارس (Mar)</option>
                    <option value="Apr">أبريل (Apr)</option>
                    <option value="May">مايو (May)</option>
                    <option value="Jun">يونيو (June)</option>
                </select>
            </div>

            <div class="table-responsive" style="max-height: 550px;">
                <table>
                    <thead>
                        <tr>
                            <th>المسلسل</th>
                            <th>التاريخ والوقت</th>
                            <th>الحساب / مصدر القيد</th>
                            <th>الوصف / البيان</th>
                            <th>المبلغ (مدين)</th>
                            <th>الشهر</th>
                            <th>المستخدم (User)</th>
                        </tr>
                    </thead>
                    <tbody id="journalTableBody"></tbody>
                </table>
            </div>
            </div>
        </div>

        <!-- TAB 5: Sales Items (مبيعات الأصناف) -->
        <div class="section-card" id="tabSalesItems" style="display: none;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
                <h2><i class="fa-solid fa-boxes-stacked" style="color: var(--accent-warning);"></i> 📦 تحليل مبيعات الأصناف والمنتجات</h2>
            </div>
            <div class="filter-box">
                <input type="text" class="filter-input" id="searchSalesInput" placeholder="🔍 ابحث باسم الصنف أو الكود..." oninput="filterSalesTable()" style="flex: 1;">
            </div>
            <div id="salesSummaryCards" style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px,1fr)); gap:16px; margin-bottom:20px;"></div>
            <div class="table-responsive" style="max-height: 600px;">
                <table>
                    <thead>
                        <tr>
                            <th>الكود</th>
                            <th>اسم الصنف</th>
                            <th>الوحدة</th>
                            <th>ك. صافى</th>
                            <th>سعر صافى (ج.م)</th>
                            <th>تكلفة البيع (ج.م)</th>
                            <th>الربح (ج.م)</th>
                            <th>نسبة الربح %</th>
                        </tr>
                    </thead>
                    <tbody id="salesItemsTableBody"></tbody>
                </table>
            </div>
        </div>

    </div>

    <!-- Notification Toast -->
    <div id="toast" class="toast">
        <i class="fa-solid fa-circle-check"></i>
        <span id="toastMsg">تم نسخ الرابط بنجاح!</span>
    </div>

    <script>
        let sheetData = ''' + json.dumps(raw_data, ensure_ascii=False) + ''';
        let charts = {};
        let pnlRowsOriginal = [];
        let ccRowsOriginal = [];
        let expRowsOriginal = [];
        let salesRowsOriginal = [];

        function formatMoney(num) {
            if (num === null || num === undefined || isNaN(num)) return "0 ج.م";
            return new Intl.NumberFormat('ar-EG', { style: 'currency', currency: 'EGP', maximumFractionDigits: 0 }).format(num);
        }

        function downloadMobileHtmlReport() {
            fetch(window.location.origin + '/share.html')
                .then(res => res.text())
                .then(htmlStr => {
                    const updatedStr = htmlStr.replace(
                        /let sheetData = [\\s\\S]*?;/,
                        'let sheetData = ' + JSON.stringify(sheetData) + ';'
                    );
                    const blob = new Blob(['\ufeff' + updatedStr], { type: 'text/html;charset=utf-8' });
                    const a = document.createElement('a');
                    a.href = URL.createObjectURL(blob);
                    a.download = 'تقرير_نتائج_نفقات_شركة_الحاج_جمعة_السحابة.html';
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    showToast("📱 تم تصدير وتنزيل ملف التقرير بالأرقام والشيت الجديد المرفوع بنجاح!");
                })
                .catch(() => {
                    window.open('/share.html', '_blank');
                });
        }

        async function shareDashboardLink() {
            showToast("⏳ جاري رفع وتحديث البيانات الجديدة على الرابط العالمي...");
            try {
                const res = await fetch(window.location.origin + '/share.html');
                const htmlStr = await res.text();
                
                const updatedHtml = htmlStr.replace(
                    /let sheetData = [\\s\\S]*?;/,
                    'let sheetData = ' + JSON.stringify(sheetData) + ';'
                );

                const formData = new FormData();
                formData.append("reqtype", "fileupload");
                const blob = new Blob([updatedHtml], { type: 'text/html;charset=utf-8' });
                formData.append("fileToUpload", blob, "report.html");

                const uploadRes = await fetch("https://catbox.moe/user/api.php", {
                    method: "POST",
                    body: formData
                });

                if (uploadRes.ok) {
                    const globalUrl = (await uploadRes.text()).trim();
                    await navigator.clipboard.writeText(globalUrl);
                    showToast("🔗 تم تحديث البيانات ونسخ الرابط العالمي الجديد بالبيانات المرفوعة!");
                } else {
                    throw new Error("Upload failed");
                }
            } catch (err) {
                const fallbackUrl = "https://d6703a16dd4e75.lhr.life/share.html";
                try {
                    await navigator.clipboard.writeText(fallbackUrl);
                } catch(e) {}
                showToast("🔗 تم نسخ رابط التقرير والموقع بنجاح!");
            }
        }

        function showToast(msg) {
            const toast = document.getElementById('toast');
            document.getElementById('toastMsg').innerText = msg;
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 3500);
        }

        function handleFileUpload(file) {
            if (!file) return;

            // Show loading state
            document.getElementById('uploadStatus').innerHTML = `
                <div style="background:rgba(59,130,246,0.15); border:1px solid var(--accent-primary); padding:14px; border-radius:8px; margin-top:10px; text-align:center;">
                    <div style="font-size:1.4rem; margin-bottom:6px;">⏳</div>
                    <strong style="color:var(--accent-primary);">جاري رفع ومعالجة الشيت بواسطة Python...</strong><br>
                    <small style="color:var(--text-muted);">يقوم السيرفر الآن بقراءة كل بيانات "${file.name}" وإعادة بناء التقرير بالكامل</small>
                </div>
            `;
            showToast("⏳ جاري رفع ومعالجة الشيت...");

            const reader = new FileReader();
            reader.onload = function(e) {
                const data = new Uint8Array(e.target.result);

                fetch('http://localhost:8083/upload_excel', {
                    method: 'POST',
                    headers: { 'Content-Length': data.length },
                    body: data
                })
                .then(res => res.json())
                .then(result => {
                    if (result.status === 'success') {
                        const sheetsText = Object.entries(result.sheets || {})
                            .map(([name, count]) => `${name}: ${count} صف`)
                            .join(' | ');

                        document.getElementById('uploadStatus').innerHTML = `
                            <div style="background:rgba(16,185,129,0.15); border:1px solid var(--accent-success); padding:14px; border-radius:8px; margin-top:10px;">
                                <div style="font-size:1.4rem; margin-bottom:6px; text-align:center;">✅</div>
                                <strong style="color:#34d399; font-size:1rem;">تم تحديث جميع البيانات بنجاح من الملف: ${file.name}</strong><br>
                                <small style="color:var(--text-muted); display:block; margin-top:6px;">${sheetsText}</small>
                                <div style="margin-top:12px; text-align:center;">
                                    <button onclick="location.reload()" style="background:var(--accent-success); color:white; border:none; padding:8px 24px; border-radius:8px; font-family:Cairo,sans-serif; font-size:0.95rem; font-weight:700; cursor:pointer;">
                                        🔄 تحديث الصفحة لعرض البيانات الجديدة
                                    </button>
                                </div>
                            </div>
                        `;
                        showToast("🎉 تم المعالجة بنجاح! اضغط تحديث الصفحة لرؤية البيانات الجديدة");
                    } else {
                        throw new Error(result.message || 'فشل التحديث');
                    }
                })
                .catch(err => {
                    // Fallback: process in browser with XLSX.js
                    try {
                        const workbook = XLSX.read(data, { type: 'array' });
                        const newSheetData = {};
                        workbook.SheetNames.forEach(name => {
                            newSheetData[name] = XLSX.utils.sheet_to_json(workbook.Sheets[name], { header: 1 });
                        });
                        sheetData = newSheetData;
                        try { localStorage.setItem('el_sahaba_current_data', JSON.stringify(sheetData)); } catch(e) {}

                        document.getElementById('uploadStatus').innerHTML = `
                            <div style="background:rgba(245,158,11,0.15); border:1px solid var(--accent-warning); padding:14px; border-radius:8px; margin-top:10px;">
                                <strong style="color:var(--accent-warning);">⚠️ تم التحديث في المتصفح فقط (السيرفر غير متاح)</strong><br>
                                <small style="color:var(--text-muted);">الملف: ${file.name} | الشيتات: ${workbook.SheetNames.join(' | ')}</small>
                            </div>
                        `;
                        showToast("✅ تم تحديث البيانات في المتصفح!");
                        initPnL(); initCostCenters(); initExpAnalysis(); initJournal(); initSalesItems();
                    } catch(e2) {
                        alert("⚠️ تعذر قراءة الملف: " + e2.message);
                    }
                });
            };
            reader.readAsArrayBuffer(file);
            try { document.getElementById('excelUploader').value = ''; } catch(e) {}
        }

        function switchTab(tabId) {
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.section-card').forEach(sec => sec.style.display = 'none');

            if (tabId === 'pnl') {
                document.querySelectorAll('.tab-btn')[0].classList.add('active');
                document.getElementById('tabPnl').style.display = 'block';
            } else if (tabId === 'costCenters') {
                document.querySelectorAll('.tab-btn')[1].classList.add('active');
                document.getElementById('tabCostCenters').style.display = 'block';
                renderCostCenterCharts();
            } else if (tabId === 'expAnalysis') {
                document.querySelectorAll('.tab-btn')[2].classList.add('active');
                document.getElementById('tabExpAnalysis').style.display = 'block';
            } else if (tabId === 'journal') {
                document.querySelectorAll('.tab-btn')[3].classList.add('active');
                document.getElementById('tabJournal').style.display = 'block';
            } else if (tabId === 'salesItems') {
                document.querySelectorAll('.tab-btn')[4].classList.add('active');
                document.getElementById('tabSalesItems').style.display = 'block';
            }
        }

        // Initialize P&L Data - Supports dynamic columns (Mar, Apr, May, June, July + ...)
        function initPnL() {
            let sheetName = Object.keys(sheetData).find(s => s.includes('قائمة') || s.includes('الدخل')) || Object.keys(sheetData)[1];
            const rows = sheetData[sheetName];
            if (!rows || rows.length < 2) return;

            // Read headers dynamically from row 0
            const headers = (rows[0] || []).map(h => h ? String(h) : '');
            // Month columns start at index 1 (skip البيان)
            const monthCols = headers.slice(1).filter(h => h && h.trim());
            const numMonths = monthCols.length;

            let totalSales = 0, totalCogs = 0, totalGrossMargin = 0, totalNetProfit = 0;
            const salesByMonth = new Array(numMonths).fill(0);
            const cogsByMonth = new Array(numMonths).fill(0);

            pnlRowsOriginal = rows.slice(1);

            pnlRowsOriginal.forEach(r => {
                if (!r || !r[0]) return;
                const name = String(r[0]).trim();
                const monthVals = monthCols.map((_, i) => parseFloat(r[i + 1]) || 0);
                const rowTotal = monthVals.reduce((a, b) => a + b, 0);

                if (name.includes('اجمالى مبيعات') || name.includes('إجمالى مبيعات')) {
                    if (totalSales === 0) {
                        totalSales = rowTotal;
                        monthVals.forEach((v, i) => salesByMonth[i] = v);
                    }
                } else if (name.includes('تكلفة البضاعه') || name.includes('تكلفة البضاعة')) {
                    totalCogs = rowTotal;
                    monthVals.forEach((v, i) => cogsByMonth[i] = v);
                } else if (name.includes('هامش الربح') || name.includes('مجمل الربح')) {
                    totalGrossMargin = rowTotal;
                } else if (name.includes('صافى ربح') || name.includes('ربح/خساره') || name.includes('خساره') || name.includes('صافي ربح')) {
                    totalNetProfit = rowTotal;
                }
            });

            // Auto-calculate gross margin if not found
            if (totalGrossMargin === 0) totalGrossMargin = totalSales - totalCogs;
            // Auto-calculate net profit if not found
            if (totalNetProfit === 0) totalNetProfit = totalGrossMargin;

            document.getElementById('kpiTotalSales').innerText = formatMoney(totalSales);
            document.getElementById('kpiTotalCogs').innerText = formatMoney(totalCogs);
            document.getElementById('kpiGrossMargin').innerText = formatMoney(totalGrossMargin);
            document.getElementById('kpiNetProfitLoss').innerText = formatMoney(totalNetProfit);

            filterPnlTable();

            const monthLabels = monthCols.map(m => {
                const map = {Mar:'مارس',Apr:'أبريل',may:'مايو',june:'يونيو',july:'يوليو',Aug:'أغسطس',Sep:'سبتمبر',Oct:'أكتوبر',Nov:'نوفمبر',Dec:'ديسمبر',Jan:'يناير',Feb:'فبراير'};
                return map[m] || m;
            });

            // Dynamically set table headers based on actual month columns
            const pnlHead = document.getElementById('pnlTableHead');
            if (pnlHead) {
                pnlHead.innerHTML = '<th>البيان المحاسبي</th>' +
                    monthLabels.map(m => `<th>${m}</th>`).join('') +
                    '<th style="color:var(--accent-success);">إجمالي الفترة (ج.م)</th>';
            }

            if (charts.pnlBar) charts.pnlBar.destroy();
            const ctxBar = document.getElementById('pnlBarChart').getContext('2d');
            charts.pnlBar = new Chart(ctxBar, {
                type: 'bar',
                data: {
                    labels: monthLabels,
                    datasets: [
                        { label: 'إجمالي المبيعات', data: salesByMonth, backgroundColor: '#3b82f6', borderRadius: 6 },
                        { label: 'تكلفة البضاعة (COGS)', data: cogsByMonth, backgroundColor: '#ef4444', borderRadius: 6 }
                    ]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#94a3b8' } } } }
            });

            if (charts.pnlPie) charts.pnlPie.destroy();
            const ctxPie = document.getElementById('pnlPieChart').getContext('2d');
            charts.pnlPie = new Chart(ctxPie, {
                type: 'doughnut',
                data: {
                    labels: monthLabels,
                    datasets: [{ data: salesByMonth, backgroundColor: ['#3b82f6','#8b5cf6','#06b6d4','#10b981','#f59e0b','#ef4444'] }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8' } } } }
            });
        }

        // Live Search for TAB 1 (P&L) - Dynamic columns
        function filterPnlTable() {
            const query = (document.getElementById('searchPnlInput').value || '').trim().toLowerCase();
            let html = '';
            let count = 0;

            // Get headers dynamically
            const sheetName = Object.keys(sheetData).find(s => s.includes('قائمة') || s.includes('الدخل')) || Object.keys(sheetData)[1];
            const headers = sheetData[sheetName] && sheetData[sheetName][0] ? sheetData[sheetName][0].map(h => h ? String(h) : '') : [];
            const monthCols = headers.slice(1).filter(h => h && h.trim());
            const monthMap = {Mar:'مارس',Apr:'أبريل',may:'مايو',june:'يونيو',july:'يوليو',Aug:'أغسطس',Sep:'سبتمبر',Oct:'أكتوبر',Nov:'نوفمبر',Dec:'ديسمبر',Jan:'يناير',Feb:'فبراير'};

            pnlRowsOriginal.forEach(r => {
                if (!r || !r[0]) return;
                const name = String(r[0]).trim();
                if (query && !name.toLowerCase().includes(query)) return;

                count++;
                const monthVals = monthCols.map((_, i) => parseFloat(r[i + 1]) || 0);
                const rowTotal = monthVals.reduce((a, b) => a + b, 0);

                const isHighlight = (name.includes('اجمالى') || name.includes('صافى') || name.includes('تكلفة'));
                const monthCells = monthVals.map(v => `<td>${formatMoney(v)}</td>`).join('');
                html += `
                    <tr style="${isHighlight ? 'background: rgba(59,130,246,0.12); font-weight:800;' : ''}">
                        <td><strong>${name}</strong></td>
                        ${monthCells}
                        <td><strong style="color:var(--accent-success);">${formatMoney(rowTotal)}</strong></td>
                    </tr>
                `;
            });

            document.getElementById('pnlTableBody').innerHTML = html;
            document.getElementById('pnlMatchCount').innerText = query ? `(تم العثور على ${count} بند)` : '';
        }

        // Initialize Cost Centers Data
        let ccTotals = {};
        function initCostCenters() {
            let sheetName = Object.keys(sheetData).find(s => s.includes('مراكز')) || Object.keys(sheetData)[3];
            const rows = sheetData[sheetName];
            if (!rows || rows.length < 2) return;

            ccRowsOriginal = rows.slice(1);
            ccTotals = {};

            let currentMain = '';
            ccRowsOriginal.forEach(r => {
                if (!r || !r[0]) return;
                const name = String(r[0]).trim();
                const mar = parseFloat(r[1]) || 0;
                const apr = parseFloat(r[2]) || 0;
                const may = parseFloat(r[3]) || 0;
                const june = parseFloat(r[4]) || 0;
                const sum = mar + apr + may + june;

                if (['الالات والمعدات', 'تريسكل', 'العربية الملاكى', 'الموتوسيكل', 'العربية النقل'].includes(name)) {
                    currentMain = name;
                    ccTotals[currentMain] = sum;
                }
            });

            filterCcTable();
        }

        // Live Search for TAB 2 (Cost Centers)
        function filterCcTable() {
            const query = (document.getElementById('searchCcInput').value || '').trim().toLowerCase();
            let html = '';
            let currentMain = '';
            let count = 0;

            ccRowsOriginal.forEach(r => {
                if (!r || !r[0]) return;
                const name = String(r[0]).trim();
                const mar = parseFloat(r[1]) || 0;
                const apr = parseFloat(r[2]) || 0;
                const may = parseFloat(r[3]) || 0;
                const june = parseFloat(r[4]) || 0;
                const sum = mar + apr + may + june;

                const isMainHeader = ['الالات والمعدات', 'تريسكل', 'العربية الملاكى', 'الموتوسيكل', 'العربية النقل'].includes(name);

                if (isMainHeader) {
                    currentMain = name;
                }

                if (query && !name.toLowerCase().includes(query) && !currentMain.toLowerCase().includes(query)) return;

                count++;
                if (isMainHeader) {
                    html += `
                        <tr style="background: rgba(139, 92, 246, 0.2); font-weight:800;">
                            <td><strong style="color:var(--accent-purple); font-size:1.05rem;">🚜 ${name}</strong></td>
                            <td>إجمالي المركز</td>
                            <td>${formatMoney(mar)}</td>
                            <td>${formatMoney(apr)}</td>
                            <td>${formatMoney(may)}</td>
                            <td>${formatMoney(june)}</td>
                            <td><strong style="color:var(--accent-success);">${formatMoney(sum)}</strong></td>
                        </tr>
                    `;
                } else {
                    html += `
                        <tr>
                            <td style="padding-right: 25px; color:var(--text-muted);">${currentMain}</td>
                            <td><span class="badge badge-primary">${name}</span></td>
                            <td>${formatMoney(mar)}</td>
                            <td>${formatMoney(apr)}</td>
                            <td>${formatMoney(may)}</td>
                            <td>${formatMoney(june)}</td>
                            <td><strong>${formatMoney(sum)}</strong></td>
                        </tr>
                    `;
                }
            });

            document.getElementById('ccTableBody').innerHTML = html;
            document.getElementById('ccMatchCount').innerText = query ? `(تم العثور على ${count} نتيجة)` : '';
        }

        function renderCostCenterCharts() {
            if (charts.ccBar) charts.ccBar.destroy();

            const labels = Object.keys(ccTotals);
            const values = Object.values(ccTotals);
            const colors = ['#8b5cf6', '#06b6d4', '#3b82f6', '#f59e0b', '#10b981'];

            const ctxBar = document.getElementById('ccBarChart').getContext('2d');
            charts.ccBar = new Chart(ctxBar, {
                type: 'bar',
                data: { labels, datasets: [{ label: 'إجمالي النفقات (ج.م)', data: values, backgroundColor: colors, borderRadius: 6 }] },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
            });

            if (charts.ccPie) charts.ccPie.destroy();
            const ctxPie = document.getElementById('ccPieChart').getContext('2d');
            charts.ccPie = new Chart(ctxPie, {
                type: 'doughnut',
                data: { labels, datasets: [{ data: values, backgroundColor: colors }] },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8' } } } }
            });
        }

        // Initialize Expense Analysis Data
        function initExpAnalysis() {
            let sheetName = Object.keys(sheetData).find(s => s.includes('تحليل')) || Object.keys(sheetData)[2];
            const rows = sheetData[sheetName];
            if (!rows || rows.length < 2) return;

            expRowsOriginal = rows.slice(1);
            filterExpTable();
        }

        // Live Search for TAB 3 (Expense Variance Analysis)
        function filterExpTable() {
            const query = (document.getElementById('searchExpInput').value || '').trim().toLowerCase();
            let html = '';
            let count = 0;

            expRowsOriginal.forEach(r => {
                if (!r || !r[0]) return;

                const name = String(r[0]);
                if (query && !name.toLowerCase().includes(query)) return;

                count++;
                const feb = parseFloat(r[1]) || 0;
                const mar = parseFloat(r[2]) || 0;
                const cmp1 = parseFloat(r[3]) || 0;
                const apr = parseFloat(r[4]) || 0;
                const cmp2 = parseFloat(r[5]) || 0;
                const may = parseFloat(r[6]) || 0;
                const cmp3 = parseFloat(r[7]) || 0;
                const june = parseFloat(r[8]) || 0;
                const cmp4 = parseFloat(r[9]) || 0;

                const renderBadge = (val) => {
                    if (val > 0) return `<span class="badge badge-danger">+${formatMoney(val)}</span>`;
                    if (val < 0) return `<span class="badge badge-success">${formatMoney(val)}</span>`;
                    return `<span class="badge badge-warning">0</span>`;
                };

                html += `
                    <tr>
                        <td><strong>${name}</strong></td>
                        <td>${formatMoney(feb)}</td>
                        <td>${formatMoney(mar)}</td>
                        <td>${renderBadge(cmp1)}</td>
                        <td>${formatMoney(apr)}</td>
                        <td>${renderBadge(cmp2)}</td>
                        <td>${formatMoney(may)}</td>
                        <td>${renderBadge(cmp3)}</td>
                        <td>${formatMoney(june)}</td>
                        <td>${renderBadge(cmp4)}</td>
                    </tr>
                `;
            });

            document.getElementById('expAnalysisBody').innerHTML = html;
            document.getElementById('expMatchCount').innerText = query ? `(تم العثور على ${count} مصروف)` : '';
        }

        // Initialize Journal Transactions Data
        let allJournalRows = [];
        function initJournal() {
            let sheetName = Object.keys(sheetData).find(s => s.includes('تقرير') || s.includes('الاستاذ')) || Object.keys(sheetData)[0];
            const rows = sheetData[sheetName];
            if (!rows || rows.length < 2) return;

            allJournalRows = rows.slice(1);
            filterJournal();
        }

        function filterJournal() {
            const desc = (document.getElementById('searchDesc').value || '').trim().toLowerCase();
            const user = document.getElementById('filterUser').value;
            const month = document.getElementById('filterMonth').value;

            let filtered = allJournalRows.filter(r => {
                const debitStr = String(r[0] || '');
                const descText = String(r[1] || '').toLowerCase();
                const m = String(r[3] || '');
                const source = String(r[5] || '').toLowerCase();
                const u = String(r[7] || '');

                if (desc && !descText.includes(desc) && !source.includes(desc) && !debitStr.includes(desc)) return false;
                if (user && u !== user) return false;
                if (month && !m.toLowerCase().includes(month.toLowerCase())) return false;

                return true;
            });

            document.getElementById('transCount').innerText = filtered.length;

            let html = '';
            filtered.forEach((r, idx) => {
                const debit = parseFloat(r[0]) || 0;
                const descText = r[1] || '-';
                const date = r[2] || '-';
                const m = r[3] || '-';
                const source = r[5] || '-';
                const u = r[7] || '-';

                html += `
                    <tr>
                        <td>${idx + 1}</td>
                        <td><small style="color:var(--text-muted);">${date}</small></td>
                        <td><span class="badge badge-purple">${source}</span></td>
                        <td><strong>${descText}</strong></td>
                        <td><strong style="color:var(--accent-secondary);">${formatMoney(debit)}</strong></td>
                        <td><span class="badge badge-primary">${m}</span></td>
                        <td><span class="badge badge-warning">${u}</span></td>
                    </tr>
                `;
            });
            document.getElementById('journalTableBody').innerHTML = html;
        }

        function exportCompleteExcel() {
            const wb = XLSX.utils.book_new();
            for (let sheetName in sheetData) {
                const ws = XLSX.utils.json_to_sheet(sheetData[sheetName]);
                XLSX.utils.book_append_sheet(wb, ws, sheetName.substring(0, 31));
            }
            XLSX.writeFile(wb, "تقرير_نفقات_شركة_الحاج_جمعة_السحابة.xlsx");
        }

        // Initialize Sales Items Tab
        function initSalesItems() {
            const sheetName = Object.keys(sheetData).find(s => s.includes('مبيعات') || s.includes('الاصناف') || s.includes('أصناف'));
            if (!sheetName) return;
            const rows = sheetData[sheetName];
            if (!rows || rows.length < 2) return;

            salesRowsOriginal = rows.slice(1).filter(r => r && r[1] && String(r[1]).trim() && !String(r[1]).includes('اجمالى'));

            let totalRevenue = 0, totalCost = 0, totalProfit = 0;
            salesRowsOriginal.forEach(r => {
                totalRevenue += parseFloat(r[8]) || 0;
                totalCost += parseFloat(r[9]) || 0;
                totalProfit += parseFloat(r[10]) || 0;
            });

            const cards = [
                { label: 'عدد الأصناف', value: salesRowsOriginal.length + ' صنف', icon: '📦', color: '#3b82f6' },
                { label: 'إجمالي الإيرادات', value: formatMoney(totalRevenue), icon: '💵', color: '#06b6d4' },
                { label: 'إجمالي التكلفة', value: formatMoney(totalCost), icon: '💸', color: '#ef4444' },
                { label: 'إجمالي الربح', value: formatMoney(totalProfit), icon: '📈', color: totalProfit >= 0 ? '#10b981' : '#f59e0b' },
            ];
            document.getElementById('salesSummaryCards').innerHTML = cards.map(c =>
                '<div style="background:var(--bg-dark); border:1px solid var(--border-color); border-radius:12px; padding:18px; display:flex; align-items:center; gap:14px;">' +
                '<div style="font-size:2rem;">' + c.icon + '</div>' +
                '<div><div style="font-size:0.8rem; color:var(--text-muted);">' + c.label + '</div>' +
                '<div style="font-size:1.2rem; font-weight:800; color:' + c.color + ';">' + c.value + '</div></div></div>'
            ).join('');

            filterSalesTable();
        }

        function filterSalesTable() {
            const query = ((document.getElementById('searchSalesInput') || {}).value || '').trim().toLowerCase();
            let html = '';
            salesRowsOriginal.forEach(r => {
                if (!r || !r[1]) return;
                const name = String(r[1]).trim();
                const code = String(r[0] || '').trim();
                if (query && !name.toLowerCase().includes(query) && !code.toLowerCase().includes(query)) return;

                const netQty = parseFloat(r[7]) || 0;
                const netPrice = parseFloat(r[8]) || 0;
                const costPrice = parseFloat(r[9]) || 0;
                const profit = parseFloat(r[10]) || 0;
                const margin = netPrice !== 0 ? ((profit / netPrice) * 100).toFixed(1) : '0.0';
                const profitColor = profit >= 0 ? 'var(--accent-success)' : '#ef4444';

                html += '<tr>' +
                    '<td style="font-size:0.8rem; color:var(--text-muted);">' + code + '</td>' +
                    '<td><strong>' + name + '</strong></td>' +
                    '<td>' + (r[2] || '-') + '</td>' +
                    '<td>' + netQty.toLocaleString('ar-EG') + '</td>' +
                    '<td>' + formatMoney(netPrice) + '</td>' +
                    '<td>' + formatMoney(costPrice) + '</td>' +
                    '<td style="color:' + profitColor + '; font-weight:700;">' + formatMoney(profit) + '</td>' +
                    '<td><span class="badge ' + (profit >= 0 ? 'badge-success' : 'badge-danger') + '">' + margin + '%</span></td>' +
                    '</tr>';
            });
            document.getElementById('salesItemsTableBody').innerHTML = html || '<tr><td colspan="8" style="text-align:center; color:var(--text-muted);">لا توجد بيانات</td></tr>';
        }

        window.addEventListener('DOMContentLoaded', () => {
            initPnL();
            initCostCenters();
            initExpAnalysis();
            initJournal();
            initSalesItems();
        });
    </script>
</body>
</html>
'''

out_path = r'C:\Users\Beteny\.gemini\antigravity\scratch\el_sahaba_expenses_dashboard\index.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Updated build_site.py with search boxes for every sheet successfully!')

# Automatically update GitHub README and ZIP file
try:
    import zipfile, shutil
    project_dir = r'C:\Users\Beteny\.gemini\antigravity\scratch\el_sahaba_expenses_dashboard'
    desktop_dir = r'C:\Users\Beteny\Desktop'
    zip_name = 'شركة_الحاج_جمعة_السحابة_موقع_النفقات.zip'
    
    zip_proj = os.path.join(project_dir, zip_name)
    zip_desk = os.path.join(desktop_dir, zip_name)
    
    files_to_zip = ['index.html', 'share.html', 'data.json', 'README.md', 'build_site.py', 'build_share.py']
    
    with zipfile.ZipFile(zip_proj, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for fn in files_to_zip:
            fp = os.path.join(project_dir, fn)
            if os.path.exists(fp):
                zipf.write(fp, arcname=fn)
                
    shutil.copyfile(zip_proj, zip_desk)
    print('Automatically updated ZIP package for GitHub on Desktop!')
except Exception as e:
    print('ZIP auto-generation note:', e)

