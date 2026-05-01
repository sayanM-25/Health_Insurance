(function () {
    const toggle = document.querySelector("[data-nav-toggle]");
    const menu = document.querySelector("[data-nav-menu]");

    if (toggle && menu) {
        toggle.addEventListener("click", function () {
            const isOpen = menu.classList.toggle("is-open");
            toggle.setAttribute("aria-expanded", String(isOpen));
        });
    }

    document.querySelectorAll(".growth-chart").forEach(function (chart) {
        const values = Array.from(chart.querySelectorAll("[data-growth-value]"))
            .map(function (node) {
                return Number(node.dataset.growthValue || 0);
            });
        const max = Math.max(1, ...values);

        chart.querySelectorAll("[data-growth-value]").forEach(function (node) {
            const value = Number(node.dataset.growthValue || 0);
            const height = Math.max(8, Math.round((value / max) * 100));
            const bar = node.querySelector("span");

            if (bar) {
                bar.style.height = height + "%";
            }
        });
    });

    document.querySelectorAll(".alert").forEach(function (alert) {
        window.setTimeout(function () {
            alert.classList.add("alert-hide");

            window.setTimeout(function () {
                alert.remove();
            }, 260);
        }, 3000);
    });
})();
