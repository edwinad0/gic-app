let isResizing = false;
let sidebar = null;
let handle = null;
let main = null;

window.onload = function () {
    sidebar = document.getElementById("sidebar");
    handle = document.getElementById("sidebar-handle");
    main = document.getElementById("main-content");

    handle.addEventListener("mousedown", function (e) {
        isResizing = true;
        document.body.style.cursor = "ew-resize";
    });

    document.addEventListener("mousemove", function (e) {
        if (!isResizing) return;

        const newWidth = Math.min(Math.max(e.clientX, 60), 400);
        sidebar.style.width = newWidth + "px";
        main.style.marginLeft = newWidth + "px";

        // toggle icon-only mode
        if (newWidth < 140) {
            sidebar.classList.add("small");
        } else {
            sidebar.classList.remove("small");
        }
    });

    document.addEventListener("mouseup", function () {
        isResizing = false;
        document.body.style.cursor = "default";
    });
};
