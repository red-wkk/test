/**
 * app.js — 用户列表页面组件
 * 负责 DOM 渲染、事件绑定和页面交互逻辑
 */

(function () {
    "use strict";

    // ---- DOM 引用 ----
    const tableBody  = document.getElementById("tableBody");
    const countEl    = document.getElementById("countEl");
    const loadingEl  = document.getElementById("loadingEl");
    const errorEl    = document.getElementById("errorEl");
    const emptyEl    = document.getElementById("emptyEl");
    const userTable  = document.getElementById("userTable");
    const refreshBtn = document.getElementById("refreshBtn");
    const footerText = document.getElementById("footerText");

    // ---- 状态映射 ----
    const STATUS_MAP = {
        1: { label: "正常",   cls: "badge-active" },
        2: { label: "禁用",   cls: "badge-disabled" },
    };

    /**
     * 渲染用户行
     * @param {Object} user
     * @returns {string} HTML 字符串
     */
    function renderRow(user) {
        const statusInfo = STATUS_MAP[user.status] || { label: "未知", cls: "badge-disabled" };

        // 对用户输入做基本转义，防止 XSS
        const username = escapeHtml(user.username);
        const email    = escapeHtml(user.email);

        return `
            <tr>
                <td>${user.id}</td>
                <td><strong>${username}</strong></td>
                <td>${email || "—"}</td>
                <td><span class="badge ${statusInfo.cls}">${statusInfo.label}</span></td>
            </tr>
        `;
    }

    /**
     * 基本的 HTML 转义
     */
    function escapeHtml(str) {
        if (!str) return "";
        const div = document.createElement("div");
        div.appendChild(document.createTextNode(str));
        return div.innerHTML;
    }

    /**
     * 隐藏所有状态区域
     */
    function hideAll() {
        loadingEl.style.display  = "none";
        errorEl.style.display    = "none";
        emptyEl.style.display    = "none";
        userTable.style.display  = "";
    }

    /**
     * 显示加载状态
     */
    function showLoading() {
        hideAll();
        loadingEl.style.display = "flex";
    }

    /**
     * 显示错误信息
     */
    function showError(message) {
        hideAll();
        errorEl.textContent = `⚠️ ${message}`;
        errorEl.style.display = "block";
        userTable.style.display = "none";
    }

    /**
     * 显示空状态
     */
    function showEmpty() {
        hideAll();
        emptyEl.style.display = "block";
    }

    /**
     * 渲染用户列表
     * @param {Array} users
     */
    function renderTable(users) {
        hideAll();

        if (!users || users.length === 0) {
            showEmpty();
            countEl.textContent = "0";
            footerText.textContent = "";
            return;
        }

        const rowsHtml = users.map(renderRow).join("");
        tableBody.innerHTML = rowsHtml;

        countEl.textContent = users.length;
        footerText.textContent = `数据来源：${users.length} 条用户记录`;
    }

    /**
     * 加载并渲染用户列表
     */
    async function loadUsers() {
        showLoading();

        try {
            const response = await fetchUsers();

            if (response && response.code === 200) {
                renderTable(response.data);
            } else {
                showError(response?.message || "接口返回异常");
            }
        } catch (err) {
            console.error("获取用户列表失败:", err);
            showError(err.message || "未知错误");
        }
    }

    /**
     * 绑定事件
     */
    function bindEvents() {
        refreshBtn.addEventListener("click", () => {
            loadUsers();
        });
    }

    /**
     * 页面初始化
     */
    async function init() {
        bindEvents();
        await loadUsers();
    }

    // 启动
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
