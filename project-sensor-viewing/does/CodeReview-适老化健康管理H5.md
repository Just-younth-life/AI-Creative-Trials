# 代码评审文档：适老化健康管理H5静态页面
文档负责人：AI产品经理

评审对象：src/demo-elder-health.html

评审时间：2026-07-18

适用定位：C端适老化AI健康产品演示页面，非中台、仅前端静态交互Demo

目标：梳理代码缺陷、体验漏洞、AI扩展短板，给出可落地改进方案

## 一、评审范围说明
1. 前端代码语法规范缺陷
2. 老年产品交互&适老化设计缺陷
3. AI健康产品专属扩展能力缺失问题
4. 工程可维护性、迭代成本问题
5. 医疗类页面合规、无障碍缺陷

## 二、P0级阻断缺陷（必须优先修复，阻碍AI功能迭代/上线）
### 1. 视图与业务逻辑强耦合，无扩展拦截层
#### 现存问题
1. 全部交互使用DOM内联 `onclick` 绑定函数，散落在每一个按钮、卡片标签内
2. 无法统一做全局拦截：埋点上报、功能灰度、AI弹窗前置拦截、权限管控
3. 新增AI语音、AI健康解读弹窗时，需要逐行修改所有DOM标签，迭代成本极高
问题代码示例：
```html
<div class="function-item-circle" onclick="switchPage('bp-page')">
<div class="active-feedback" onclick="showAlert('即将上线','血糖记录功能即将上线，敬请期待')">血糖自测</div>
<button onclick="showAlert('正在呼叫 120','模拟呼叫')">一键呼叫120</button>

## 改进方向
### 移除全部行内 onclick，统一在 JS 内使用事件委托绑定
封装全局点击拦截中间件，预留 AI 逻辑插入入口

<!-- HTML 移除onclick，增加自定义标识data-xxx -->
<div class="function-item-circle" data-target-page="bp-page">
  <div class="function-circle-box" style="background:#4CAF50;"><span class="function-icon-white">🩺</span></div>
  <span class="function-label-bold">测血压</span>
</div>
// 全局事件绑定，统一拦截埋点/AI前置提示
document.querySelectorAll("[data-target-page]").forEach(item=>{
  item.addEventListener('click',(e)=>{
    const pageId = e.currentTarget.dataset.targetPage
    trackEvent('page_click', { pageId }) // 统一埋点
    // 预留AI智能提醒拦截逻辑
    // if(aiNeedPopTip(pageId)) return;
    switchPage(pageId)
  })
})
2. 业务数据全部硬编码在 HTML，无统一数据模型，无法对接 AI 健康模块
##现存问题
用户名、血压数据、用药记录、紧急联系人、地址、历史健康指标全部写死 DOM；
无全局 JS 数据仓库，AI 慢病分析、AI 周报、AI 用药问答无法读取用户档案。
问题代码示例：
<h1 class="text-[32px] font-bold flex items-center gap-2-mt-2">
<iconify-icon icon="solar:shield-check-bold-duotone" width="36"></iconify-icon>欢迎回家，张伯伯
</h1>
<p class="text-[20px] text-gray-700">上次测量：<span class="font-bold">128/82 mmHg</span></p>
<p>苯磺酸氨氯地平片 每日1次，每次1片</p>
##改进方向
JS 顶层定义全局用户健康数据仓库，统一管理所有业务变量
// 全局统一数据仓库，AI模块可直接读取
const userHealthStore = {
  baseInfo: {name:"张伯伯", age:76, address:"北京市朝阳区XX街道XX小区3号楼1单元802"},
  bloodRecord: [{high:128, low:82, date:"2026-07-18"}],
  medicineList: [{name:"苯磺酸氨氯地平片", time:"14:30", dosage:"每日1次，每次1片", finish:false}],
  emergencyContacts: [
    {name:"李建国", relation:"儿子", phone:"138****5678"},
    {name:"王芳", relation:"女儿", phone:"139****1234"}
  ]
}
3. 三种样式体系混用，视觉规范无法统一管控
##现存问题
原生 CSS 自定义样式 + Tailwind class + DOM 行内 style 三套写法混杂
颜色、尺寸硬编码，无全局主题变量，无法一键切换适老化大号字体 / 高对比模式
<!-- 行内硬编码颜色，无法统一管理 -->
<div class="function-circle-box" style="background:#4CAF50;">
/* 原生css全局样式 */
.sos-gradient {background:linear-gradient(180deg,#E63E3E,#C62828);}
##改进方向
废弃所有行内 style，颜色统一放入 tailwind.config 主题扩展；
tailwind.config = {
  theme:{
    extend:{
      colors:{
        healthGreen: '#7AB89B',
        dangerRed: '#E63E3E',
        warmOrange: '#F8B88A'
      }
    }
  }
}
<div class="function-circle-box bg-healthGreen">
4. 存在破坏性 DOM 操作，页面结构不稳定
##现存问题
用药页面点击按钮直接覆盖父容器 innerHTML，销毁原有 DOM 结构；后续叠加 AI 服药问答、用药知识库模块会直接崩溃。
<button class="active-feedback flex-1 h-[60px] bg-[#4A90A0] text-white text-[22px] font-bold rounded-[20px]" onclick="this.parentElement.innerHTML='<div class=\'w-full h-[60px] bg-green-50 text-green-600 flex items-center justify-center rounded-2xl text-[20px] font-bold\'>✅ 今日已服用</div>'">标记已服用</button>

##改进方向
通过数据状态控制显示隐藏，使用 class 切换状态，禁止直接覆盖 DOM。
<!-- 增加状态标识，不销毁DOM -->
<button class="active-feedback medicine-finish-btn w-full h-[60px] bg-[#4A90A0] text-white text-[22px] font-bold rounded-[20px]" data-medicine-id="1">标记已服用</button>
<div class="finish-tip hidden w-full h-[60px] bg-green-50 text-green-600 flex items-center justify-center rounded-2xl text-[20px] font-bold">✅ 今日已服用</div>
document.querySelector('.medicine-finish-btn').addEventListener('click', function(){
  this.classList.add('hidden');
  this.nextElementSibling.classList.remove('hidden');
  // 更新全局数据仓库状态，同步给AI模块
  userHealthStore.medicineList[0].finish = true;
  trackEvent('medicine_finish', {medicineId: this.dataset.medicineId})
})
5. 表单无数值校验，产生脏数据干扰 AI 健康分析
##现存问题
血压输入框仅限制数字，未做区间校验，可输入 0、负数、300 高压等无效数值；AI 读取脏数据会生成错误健康诊断建议。
<input class="w-full h-[60px] bg-gray-50 border-2 border-gray-100 rounded-2xl px-6 text-[28px] font-bold focus:border-[#E8634A] focus:outline-none focus:bg-white transition-all" placeholder="请输入数字" type="number"/>
##改进方向
封装通用数字校验工具函数；
保存前拦截非法数值，弹出 AI 友好提示文案。
// 血压数值校验工具
function checkBloodValue(high, low){
  if(high < 60 || high > 220) return {pass:false, msg:"高压数值范围请输入60~220之间"}
  if(low < 40 || low > 140) return {pass:false, msg:"低压数值范围请输入40~140之间"}
  return {pass:true}
}
function saveRecord() {
  const highVal = document.querySelector('input[name="high"]').value
  const lowVal = document.querySelector('input[name="low"]').value
  const checkRes = checkBloodValue(Number(highVal), Number(lowVal))
  if(!checkRes.pass){
    showAlert('输入数值不规范', checkRes.msg)
    return;
  }
  // 正常保存逻辑
  const toast = document.getElementById('toast');
  toast.classList.remove('hidden');
  setTimeout(()=>{toast.classList.add('hidden');switchPage('home-page');},1500);
}

## 三、P1 级适老化 & 无障碍缺陷（二期迭代修复，老年核心体验问题）
1. 无完整无障碍语义化，不支持手机读屏 / AI 语音朗读
##现存问题
大量使用 div/span 模拟按钮、勾选框，无原生<button>、<label>；
图标按钮、弹窗无 aria-label 无障碍描述；
自定义待办勾选框无法被屏幕阅读器识别状态。
<span class="todo-circle" onclick="toggleTodo(this);event.stopPropagation();"></span>
##改进方向
所有可点击交互元素统一使用原生 button；
图标、无文字按钮补充 aria 说明，适配系统 AI 朗读；
勾选组件使用原生 checkbox 封装。
<label class="flex items-center">
  <input type="checkbox" class="todo-circle-input mr-4">
  <span class="todo-text text-[20px] font-medium text-[#2D2D2D]">14:30 服用降压药</span>
</label>
function showAlert(title, content) {
  document.getElementById('modal-title').innerText = title;
  document.getElementById('modal-content').innerText = content;
  const overlay = document.getElementById('modal-overlay')
  overlay.classList.remove('hidden');
  // 锁定页面滚动
  document.body.style.overflow = 'hidden'
}
function closeModal() {
  document.getElementById('modal-overlay').classList.add('hidden');
  // 释放滚动
  document.body.style.overflow = ''
}

## 四、三期优化，赋能 AI 功能落地
1. 无独立 AI 内容渲染容器
##现存问题
健康资讯、健康解读全部静态写死页面，没有预留独立区块渲染 AI 动态生成的个性化健康建议、慢病解读、周报内容。
##改进方向
统一新增专用容器，用于承载 AI 输出文本、图表。
<!-- AI专属渲染容器，全局统一 -->
<div id="ai-report-block" class="hidden bg-white p-5 rounded-[20px] card-shadow my-6">
  <h3 class="text-[20px] font-bold mb-4">AI健康解读</h3>
  <div id="ai-report-content"></div>
</div>
// 全局埋点工具，AI模型数据采集统一入口
function trackEvent(eventName, params={}){
  // 可对接后端埋点上报接口
  console.log('埋点上报', eventName, { time: new Date().getTime(), ...params })
}
<!-- AI语音悬浮按钮预留位 -->
<div id="ai-voice-btn" class="fixed bottom-[230px] right-[16px] w-[64px] h-[64px] rounded-full bg-healthGreen shadow-lg hidden flex items-center justify-center z-[999]">
  <iconify-icon icon="solar:microphone-bold" width="32" class="text-white"></iconify-icon>
</div>
<!-- 全局医疗合规提示 -->
<div class="text-[14px] text-gray-500 mt-8 p-4 border-t border-gray-200">
  温馨提示：本平台健康数据、AI解读内容仅供日常参考，不能替代执业医师诊断，身体不适请及时前往医院就诊。
</div>
