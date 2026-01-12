async function getLcscIdFromTab(tabId) {
  return chrome.tabs.sendMessage(tabId, { type: "GET_LCSC_ID" });
}

async function exportPart(lcscId) {
  if (!lcscId) {
    throw new Error("No LCSC part number found on the page.");
  }

  return chrome.runtime.sendNativeMessage("com.easyeda2kicad", {
    lcsc_id: lcscId,
    full: true
  });
}

chrome.action.onClicked.addListener(async (tab) => {
  if (!tab?.id) {
    return;
  }

  try {
    const response = await getLcscIdFromTab(tab.id);
    const exportResponse = await exportPart(response?.lcscId);
    if (exportResponse?.status !== "ok") {
      console.warn("easyeda2kicad export failed:", exportResponse);
    }
  } catch (error) {
    console.error("easyeda2kicad extension error:", error);
  }
});
