function loadTasks() {
    $.ajax({
        url: "/task/", // Django 视图 URL
        type: "GET",
        headers: { "X-Requested-With": "XMLHttpRequest" },
        success: function (response) {
            let taskList = $("#task-list");
            taskList.empty();

            if (response.tasks.length === 0) {
                taskList.append('<li class="p-4 text-gray-500">暂无任务</li>');
                return;
            }

            response.tasks.forEach(task => {
                let statusColor = task.status === "已逾期" ? "text-red-500" :
                    task.status === "已完成" ? "text-green-500" :
                        "text-gray-700";

                taskList.append(`
    <li x-data="{ open: false }" class="p-4 border-b" id="task-${task.id}">
        <div class="flex justify-between items-center cursor-pointer" @click="open = !open">
            <div>
                <h2 class="text-lg font-semibold text-blue-600">${task.name}</h2>
                <p class="text-sm text-gray-500">来源: ${task.source}</p>
                <p class="text-sm text-gray-500">截止时间: ${task.deadline}</p>
                <p class="text-sm ${statusColor}" id="task-status-${task.id}">
                    状态: ${task.status}
                </p>
            </div>
        </div>
        <div x-show="open" class="mt-2 p-4 bg-gray-100 rounded-md">
            <p class="text-gray-700"><strong>描述:</strong> ${task.description}</p>
            <div class="flex justify-end space-x-2 mt-2">
                <a href="/tasks/${task.id}/edit/" class="text-blue-500">编辑</a>
                <a href="/tasks/${task.id}/delete/" class="text-red-500">删除</a>
            </div>
        </div>
        <input type="checkbox" class="w-5 h-5 text-green-500 cursor-pointer" ${task.status === "已完成" ? "checked" : ""}
            onchange="updateTaskStatus(${task.id}, this)">
    </li>
    `);
            });
        },
        error: function () {
            alert("任务加载失败！");
        }
    });
}

function updateTaskStatus(taskId, checkbox) {
    const isChecked = checkbox.checked;
    const task_status = document.getElementById(`task-status-${taskId}`);
    fetch(`/task/update_status/${taskId}/`, {  // 发送请求到 Django 后端
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()  // 发送 CSRF 令牌
        },
        body: JSON.stringify({ checked: isChecked })  // 发送 JSON 数据
    })
        .then(response => response.json())
        .then(data => {
            loadTasks();
        })
        .catch(error => console.error("错误:", error));
}
function getCSRFToken() {
    return document.cookie.split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
}