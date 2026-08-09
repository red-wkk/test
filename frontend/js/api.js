/**
 * api.js — 前端 API 封装模块
 * 提供调用后端接口的基础函数
 */

const API_BASE_URL = "http://localhost:8000";

/**
 * 通用请求函数
 * @param {string} path   - 接口路径（如 /api/users）
 * @param {object} options - fetch 选项
 * @returns {Promise<any>}
 */
async function request(path, options = {}) {
    const url = `${API_BASE_URL}${path}`;

    const defaultHeaders = {
        "Content-Type": "application/json",
    };

    const config = {
        ...options,
        headers: {
            ...defaultHeaders,
            ...options.headers,
        },
    };

    try {
        const response = await fetch(url, config);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const result = await response.json();
        return result;
    } catch (error) {
        // 网络错误或超时
        if (error.name === "TypeError" && error.message.includes("fetch")) {
            throw new Error("网络连接失败，请检查后端服务是否已启动。");
        }
        throw error;
    }
}

/**
 * 获取用户列表
 * @returns {Promise<{code: number, message: string, data: Array}>}
 */
async function fetchUsers() {
    return request("/api/users");
}

/**
 * 健康检查
 * @returns {Promise<{status: string, mock_mode: boolean}>}
 */
async function healthCheck() {
    return request("/api/health");
}
