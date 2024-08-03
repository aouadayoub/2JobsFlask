import ExtractSkills


def ExtractData(path):

    #formation = ExtractFormation.GetFormationResume(path)

    #Experiences = ExtractExperiences.GetEXperiencesResume(path)

    Skills = ExtractSkills.GetSkillsResume(path)

    return Skills


# PATH_FILE = "D:\HAMZA M2\Fati_CV.pdf"
# formation, experiences, skills = ExtractData(PATH_FILE)

# print("====================== formation =======================")
# print(formation)
# print("====================== Experiences =======================")
# print(experiences)
# print("====================== skills =======================")
# print(skills)