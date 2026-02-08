import re

# Read the file
with open('public/user.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the showGroupBadge issue in form submission
content = content.replace(
    'if (showGroupBadge && prize.groupId) {',
    'if (prize.groupId) {'
)

# Write back
with open('public/user.js', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed showGroupBadge issue!')
