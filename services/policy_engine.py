import json

# Load policy from JSON file
with open("policy.json") as f:
    policy = json.load(f)

# 🔍 Validate expense
def validate(role, expense_type, amount):
    role = role.lower()
    expense_type = expense_type.lower()

    # Employee rules
    if role == "employee":
        if expense_type == "travel" and amount <= 2000:
            return True
        elif expense_type == "food" and amount <= 500:
            return True
        elif expense_type == "hotel" and amount <= 3000:
            return True

    # Admin can approve anything
    elif role == "admin":
        return True

    return False