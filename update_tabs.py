import re

# Read the file
with open('public/user.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update DOM Elements section - add new tab elements
old_dom = '''// ===== DOM Elements =====
const prizesList = document.getElementById('prizesList');
const emptyState = document.getElementById('emptyState');
const labelsContainer = document.getElementById('labelsContainer');'''

new_dom = '''// ===== DOM Elements =====
const labelsContainer = document.getElementById('labelsContainer');

// Tab elements
const prizeTabs = document.querySelectorAll('.prize-tab');
const tabContents = document.querySelectorAll('.prize-tab-content');

const prizesListUnlimited = document.getElementById('prizesListUnlimited');
const prizesListLimited = document.getElementById('prizesListLimited');
const prizesListWinners = document.getElementById('prizesListWinners');

const emptyStateUnlimited = document.getElementById('emptyStateUnlimited');
const emptyStateLimited = document.getElementById('emptyStateLimited');
const emptyStateWinners = document.getElementById('emptyStateWinners');'''

content = content.replace(old_dom, new_dom)

# 2. Add tab switching logic after DOMContentLoaded
old_init = '''document.addEventListener('DOMContentLoaded', () => {
    renderLabels();
    renderPrizes();
    updateEmptyState();
});'''

new_init = '''document.addEventListener('DOMContentLoaded', () => {
    renderLabels();
    renderPrizes();
    setupTabs();
});

// ===== Tab Switching =====
function setupTabs() {
    prizeTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.dataset.tab;
            
            prizeTabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            tab.classList.add('active');
            document.getElementById(`tab-${targetTab}`).classList.add('active');
        });
    });
}'''

content = content.replace(old_init, new_init)

# 3. Replace renderPrizes function to render to different tabs
old_render_start = content.find('// ===== Render Prizes =====')
old_render_end = content.find('// ===== Create Group Section =====')
old_render_section = content[old_render_start:old_render_end]

new_render_section = '''// ===== Render Prizes =====
function renderPrizes() {
    // Clear all lists
    prizesListUnlimited.innerHTML = '';
    prizesListLimited.innerHTML = '';
    prizesListWinners.innerHTML = '';
    
    // Separate prizes by type
    const unlimitedPrizes = [];
    const limitedPrizes = [];
    const winnerPrizes = [];
    
    prizes.forEach(prize => {
        if (prize.winner) {
            winnerPrizes.push(prize);
        } else if (prize.groupId) {
            const group = getGroupById(prize.groupId);
            if (group) {
                if (group.maxPrizesPerPerson >= 999) {
                    unlimitedPrizes.push(prize);
                } else if (group.maxPrizesPerPerson === 1) {
                    limitedPrizes.push(prize);
                } else {
                    // Other limits go to limited tab
                    limitedPrizes.push(prize);
                }
            }
        } else {
            // No group = unlimited
            unlimitedPrizes.push(prize);
        }
    });
    
    // Render unlimited prizes
    unlimitedPrizes.forEach(prize => {
        const prizeCard = createPrizeCard(prize, true, 'unlimited');
        prizesListUnlimited.appendChild(prizeCard);
    });
    
    // Render limited prizes
    limitedPrizes.forEach(prize => {
        const prizeCard = createPrizeCard(prize, true, 'limited');
        prizesListLimited.appendChild(prizeCard);
    });
    
    // Render winner prizes
    winnerPrizes.forEach(prize => {
        const prizeCard = createPrizeCard(prize, true, 'winners');
        prizesListWinners.appendChild(prizeCard);
    });
    
    // Update empty states
    emptyStateUnlimited.style.display = unlimitedPrizes.length === 0 ? 'block' : 'none';
    emptyStateLimited.style.display = limitedPrizes.length === 0 ? 'block' : 'none';
    emptyStateWinners.style.display = winnerPrizes.length === 0 ? 'block' : 'none';
}

'''

content = content[:old_render_start] + new_render_section + content[old_render_end:]

# 4. Update createPrizeCard signature and add entry button
content = content.replace(
    'function createPrizeCard(prize, showGroupBadge = true) {',
    'function createPrizeCard(prize, showGroupBadge = true, tabType = "unlimited") {'
)

# 5. Add entry button to prize card content (find the section with "คลิกเพื่อดูรายละเอียด")
old_card_footer = '''            <div style="text-align: center; margin-top: 1rem; padding: 0.75rem; background: rgba(102, 126, 234, 0.1); border-radius: 0.5rem; color: var(--text-secondary); font-size: 0.9rem;">
                👆 คลิกเพื่อดูรายละเอียด
            </div>'''

new_card_footer = '''            <div class="prize-card-actions" style="margin-top: 1rem; display: flex; gap: 0.5rem;">'''

# This will be added dynamically based on prize status

# Write back
with open('public/user.js', 'w', encoding='utf-8') as f:
    f.write(content)

print('File updated successfully!')
