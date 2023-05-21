chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
        title: "Download",
        contexts: ["link"],
        id: "saveFile"
    });

    chrome.contextMenus.create({
        title: "Open in VLC",
        contexts: ["link"],
        id: "openInVLC"
    });
});

chrome.contextMenus.onClicked.addListener((info) => {
    const { menuItemId, linkUrl } = info;

    if (menuItemId === "saveFile") {
        sendToFlask(linkUrl, "trigger-save");
    } else if (menuItemId === "openInVLC") {
        sendToFlask(linkUrl, "trigger-vlc");
    }
});

function sendToFlask(magnetLink, endpoint) {
    const formData = new FormData();
    formData.append("magnet_link", magnetLink);

    fetch("http://localhost:5000/" + endpoint, {
        method: "POST",
        body: formData
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error("Action triggered failed");
            }
        })
        .then(data => {
            if (endpoint === "trigger-save") {
                handleSaveFile(data.download_links);
            }
        })
        .catch(error => {
            console.error("Error sending request:", error);
        });
}

function handleSaveFile(downloadLinks) {
    if (downloadLinks && downloadLinks.length > 0) {
        chrome.downloads.download({ url: downloadLinks });
    }
}

