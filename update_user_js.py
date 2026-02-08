import re

# Read the file
with open('public/user.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace renderPrizes function
old_render = '''function renderPrizes() {
    prizesList.innerHTML = '';

    prizes.forEach(prize => {
        const prizeCard = createPrizeCard(prize);
        prizesList.appendChild(prizeCard);
    });
    
    updateEmptyState();
}'''

new_render = '''function renderPrizes() {
    prizesList.innerHTML = '';

    const groupedPrizes = {};
    const ungroupedPrizes = [];
    
    prizes.forEach(prize => {
        if (prize.groupId) {
            if (!groupedPrizes[prize.groupId]) {
                groupedPrizes[prize.groupId] = [];
            }
            groupedPrizes[prize.groupId].push(prize);
        } else {
            ungroupedPrizes.push(prize);
        }
    });
    
    Object.keys(groupedPrizes).forEach(groupId => {
        const group = getGroupById(parseInt(groupId));
        if (!group) return;
        
        const groupSection = createGroupSection(group, groupedPrizes[groupId]);
        prizesList.appendChild(groupSection);
    });
    
    if (ungroupedPrizes.length > 0) {
        ungroupedPrizes.forEach(prize => {
            const prizeCard = createPrizeCard(prize, true);
            prizesList.appendChild(prizeCard);
        });
    }
    
    updateEmptyState();
}'''

content = content.replace(old_render, new_render)

# Add createGroupSection function after updateEmptyState
insert_pos = content.find('// ===== Create Prize Card =====')
group_function = '''
// ===== Create Group Section =====
function createGroupSection(group, groupPrizes) {
    const section = document.createElement('div');
    section.className = 'group-section';
    
    const limitText = group.maxPrizesPerPerson === 1 
        ? 'สุ่มได้ 1 ชิ้น' 
        : group.maxPrizesPerPerson >= 999 
            ? 'สุ่มได้ไม่จำกัด' 
            : `สุ่มได้ ${group.maxPrizesPerPerson} ชิ้น`;
    
    section.innerHTML = `
        <div class="group-header" style="background: ${group.color}; padding: 1rem 1.5rem; border-radius: 0.75rem; margin-bottom: 1.5rem; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h3 style="margin: 0; font-size: 1.3rem; font-weight: 600; color: white;">${group.name}</h3>
                <p style="margin: 0.25rem 0 0 0; font-size: 0.9rem; color: rgba(255, 255, 255, 0.9);">${limitText}</p>
            </div>
            <div style="background: rgba(255, 255, 255, 0.2); padding: 0.5rem 1rem; border-radius: 0.5rem; font-weight: 600; color: white;">
                ${groupPrizes.length} ชิ้น
            </div>
        </div>
        <div class="group-prizes-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1.5rem; margin-bottom: 2rem;">
        </div>
    `;
    
    const gridContainer = section.querySelector('.group-prizes-grid');
    groupPrizes.forEach(prize => {
        const prizeCard = createPrizeCard(prize, false);
        gridContainer.appendChild(prizeCard);
    });
    
    return section;
}

'''

content = content[:insert_pos] + group_function + content[insert_pos:]

# Update group badge condition
content = content.replace(
    '    if (prize.groupId) {',
    '    if (showGroupBadge && prize.groupId) {'
)

# Add white color to group badge
content = content.replace(
    'font-weight: 600;">',
    'font-weight: 600; color: white;">',
    1
)

# Write back
with open('public/user.js', 'w', encoding='utf-8') as f:
    f.write(content)

print('File updated successfully!')
