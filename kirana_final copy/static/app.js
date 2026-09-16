document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatBox = document.getElementById('chat-box');
    const sendBtn = document.querySelector('.send-btn');
    const resetBtn = document.getElementById('reset-btn');
    const actionBtns = document.querySelectorAll('.action-btn');
    const marketInput = document.getElementById('market-input');
    const marketBtn = document.getElementById('market-btn');
    const marketPriceCard = document.getElementById('market-price-card');

    let sessionId = localStorage.getItem('kirana_chat_id');
    if (!sessionId) {
        sessionId = 'web-user-' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('kirana_chat_id', sessionId);
    }

    marked.setOptions({
        breaks: true,
        gfm: true
    });

    fetchStoreSummary();

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = chatInput.value.trim();
        if (!message) return;

        addMessageToUI(message, 'user');
        chatInput.value = '';
        setLoadingState(true);

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ chat_id: sessionId, message })
            });

            const data = await response.json();
            if (data.success) {
                addMessageToUI(data.response, 'assistant', data.artifacts);
                fetchStoreSummary();
            } else {
                addMessageToUI('❌ Sorry, I encountered an error: ' + data.error, 'assistant');
            }
        } catch (error) {
            console.error('Chat error:', error);
            addMessageToUI('❌ Failed to communicate with the server.', 'assistant');
        } finally {
            setLoadingState(false);
        }
    });

    marketBtn.addEventListener('click', () => fetchMarketPrice());
    marketInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            fetchMarketPrice();
        }
    });

    resetBtn.addEventListener('click', async () => {
        if (!confirm('Are you sure you want to reset the current session and clear drafts?')) return;

        try {
            const response = await fetch(`/api/session/${sessionId}/reset`, { method: 'POST' });
            const data = await response.json();
            if (data.success) {
                chatBox.innerHTML = '';
                addMessageToUI('Session has been reset. How can I help you anew?', 'assistant');
                fetchStoreSummary();
            }
        } catch (error) {
            console.error('Reset error:', error);
        }
    });

    actionBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const query = btn.getAttribute('data-query');
            if (query) {
                chatInput.value = query;
                chatForm.dispatchEvent(new Event('submit'));
            }
        });
    });

    function addMessageToUI(text, sender, artifacts = []) {
        const loadingIndicator = document.getElementById('loading-indicator');
        if (loadingIndicator) loadingIndicator.remove();

        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}-msg`;

        const avatar = document.createElement('div');
        avatar.className = 'avatar';
        avatar.innerHTML = sender === 'user' ? '<i class="fa-solid fa-user"></i>' : '<i class="fa-solid fa-robot"></i>';

        const content = document.createElement('div');
        content.className = 'msg-content';

        if (sender === 'assistant') {
            const rawHtml = marked.parse(text);
            content.innerHTML = DOMPurify.sanitize(rawHtml);

            if (artifacts && artifacts.length > 0) {
                const artifactsContainer = document.createElement('div');
                artifactsContainer.style.marginTop = '1rem';

                artifacts.forEach((art) => {
                    const iconClass = art.type === 'pdf' ? 'fa-file-pdf pdf' : 'fa-file-powerpoint pptx';
                    const link = document.createElement('a');
                    link.href = art.url;
                    link.target = '_blank';
                    link.className = 'artifact-card';
                    link.innerHTML = `
                        <i class="fa-solid ${iconClass} artifact-icon"></i>
                        <div class="artifact-details">
                            <span class="artifact-name">${art.name}</span>
                            <span class="artifact-action">Click to view/download</span>
                        </div>
                    `;
                    artifactsContainer.appendChild(link);
                });

                content.appendChild(artifactsContainer);
            }
        } else {
            content.textContent = text;
        }

        msgDiv.appendChild(avatar);
        msgDiv.appendChild(content);
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function setLoadingState(isLoading) {
        sendBtn.disabled = isLoading;
        chatInput.disabled = isLoading;

        if (isLoading) {
            const loadingIndicator = document.createElement('div');
            loadingIndicator.id = 'loading-indicator';
            loadingIndicator.className = 'message assistant-msg';
            loadingIndicator.innerHTML = `
                <div class="avatar"><i class="fa-solid fa-robot"></i></div>
                <div class="msg-content loading-indicator-content" style="padding: 1rem;">
                    <div class="loading-indicator">
                        <div class="dot"></div><div class="dot"></div><div class="dot"></div>
                    </div>
                </div>
            `;
            chatBox.appendChild(loadingIndicator);
            chatBox.scrollTop = chatBox.scrollHeight;
        } else {
            chatInput.focus();
        }
    }

    async function fetchMarketPrice() {
        const product = (marketInput.value || '').trim();
        if (!product) {
            marketPriceCard.innerHTML = '<div class="mini-label">Live product insight</div><p>Enter a product name to compare local and market prices.</p>';
            return;
        }

        try {
            const response = await fetch(`/api/market-price?product=${encodeURIComponent(product)}`);
            const data = await response.json();

            if (data.success && data.answer) {
                const dbText = data.database_reference ? `Store: ₹${data.database_reference.store_sell_price.toFixed(2)}` : 'Store: no exact match';
                const marketText = `Market MRP: ₹${(data.market?.market_mrp || 0).toFixed(2)}`;
                marketPriceCard.innerHTML = `
                    <div class="mini-label">${data.product_name}</div>
                    <p>${data.answer}</p>
                    <div class="market-stat-row"><span>${dbText}</span><span>${marketText}</span></div>
                `;
            } else {
                marketPriceCard.innerHTML = `<div class="mini-label">Market check</div><p>Unable to fetch pricing data right now.</p>`;
            }
        } catch (error) {
            console.error('Market price fetch error:', error);
            marketPriceCard.innerHTML = '<div class="mini-label">Market check</div><p>Unable to fetch pricing data right now.</p>';
        }
    }

    async function fetchStoreSummary() {
        try {
            const response = await fetch(`/api/store/summary?chat_id=${sessionId}`);
            const data = await response.json();

            if (data.success) {
                document.getElementById('summary-revenue').textContent = `₹${(data.today_revenue || 0).toFixed(2)}`;
                document.getElementById('summary-bills').textContent = data.today_bills || 0;
                document.getElementById('summary-low-stock').textContent = data.low_stock_count || 0;
                document.getElementById('summary-khata').textContent = `₹${(data.total_khata_outstanding || 0).toFixed(2)}`;
            }
        } catch (error) {
            console.error('Failed to fetch store summary:', error);
        }
    }
});
