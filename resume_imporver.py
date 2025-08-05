def improve_resume(text):
    suggestions = []
    if len(text) < 300:
        suggestions.append("Resume appears short. Add more content, like projects and experience.")
    if "experience" not in text.lower():
        suggestions.append("Add a section on your work experience.")
    if "project" not in text.lower():
        suggestions.append("Mention technical or academic projects.")
    if "skills" not in text.lower():
        suggestions.append("Include a skills section with relevant tools and technologies.")
    return suggestions
