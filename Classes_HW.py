#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Для начала нужно описать класс студента. У каждого студента должны быть следующие атрибуты класса:
# имя
# фамилия
# пол
# Без указания значений этих аттрибутов не должно быть возможности создать экземпляр класса.

class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        """Мы обязательно должны знать, какие курсы студент уже прошел. Добавим и такой атрибут.
        Учитывая, что мы хотим изначально присвоить атрибуту класса изменяемый тип данных (пустой список),
        то данный способ позволит инициализировать этот атрибут для каждого экземпляра по отдельности 
        и у каждого студента будут свои пройденные курсы.
        """
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
    
        
    def rate_lecturer(self, lecturer, course, grade):
        """ Метод выставления оценок лекторам 
        (оценки по 10-балльной шкале, хранятся в атрибуте-словаре у Lecturer, в котором ключи – названия курсов,
        а значения – списки оценок). Лектор при этом должен быть закреплен за тем курсом, на который записан студент.
        """
        if (isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached):
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'
    
    def student_avg_grade(self):
        """Метод расчета средней оценки за домашние задания по всем курсам """
        list_grade = self.grades.values()
        sum_grade = 0
        for grade in list_grade:
            sum_grade += sum(grade)
            return sum_grade / len(grade)
        
    def __str__(self):
        courses_in_progress_string = ', '.join(self.courses_in_progress)
        finished_courses_string = ', '.join(self.finished_courses)
        res = f'Имя: {self.name}\n' \
              f'Фамилия: {self.surname}\n' \
              f'Средняя оценка за домашние задания: {self.student_avg_grade()}\n' \
              f'Курсы в процессе изучения: {courses_in_progress_string}\n' \
              f'Завершенные курсы: {finished_courses_string}'
        return res
    
    def __lt__(self, other_student):
        """Создаём метод, который сравнивает (через оператор сравнения <=) между собой студентов по средней оценке 
        за домашние задания.""" 
        if isinstance(other_student, Student):
            return self.student_avg_grade() < other_student.student_avg_grade()

    
# Какое учебное заведение без преподавателей? Объявим соответствующий класс (у преподавателей есть закрепленный за ними список курсов) 

class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []    
        
# Класс Lecturer наследует имя, фамилия и список закрепленные курсы от родительского класса Mentor.

class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}
    
    def avg_grade(self):
        """ Метод вычисления средней оценки студентов лектора по тому курсу, который он преподает """
        list_grade = self.grades.values()
        sum_grade = 0
        for grade in list_grade:
            sum_grade += sum(grade)
            return float(sum_grade / len(grade))
        
    def __str__(self):
        return f' Имя: {self.name} \n Фамилия: {self.surname} \n Средняя оценка за лекции: {self.avg_grade()}'  

    
    def __lt__(self, other_lecturer): 
        """Создаём метод, который сравнивает (через оператор сравнения <=) между собой лекторов по средней оценке 
        от студентов.""" 
        if isinstance(other_lecturer, Lecturer): 
            return self.avg_grade() < other_lecturer.avg_grade()

# Класс Reviewer наследует имя, фамилия и список закрепленные курсы от родительского класса Mentor.

class Reviewer(Mentor): #эксперты, проверяющие домашние задания
        
    # И самое главное – реализуем взаимодействие классов на основе выставления преподавателями оценок студентам.

    def rate_hw(self, student, course, grade):
        """ Метод, который будет проверять, что оценка выставляется именно экземпляру класса Student, 
        при этом преподаватель должен быть прикреплен к соответствующему курсу, а студент должен его проходить. 
        Только в таком случае оценка будет добавляться в словарь, иначе будем получать ошибку.
        """
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'
        
    def __str__(self):
        return f'Имя: {self.name} \n Фамилия: {self.surname}'



# #### Students

# In[4]:


# создадим по экземпляру наших классов и проверим содержимое атрибутов. 
# Добавим возможность хранить информацию студентов об оценках (словарь) и о списке курсов, которые сейчас изучаются.

best_student = Student('Ruoy', 'Eman', 'your_gender')
best_student.finished_courses += ['Git']
best_student.courses_in_progress += ['Python']
best_student.grades['Git'] = [10, 10, 10, 10, 10]
best_student.grades['Python'] = [10, 10]


# In[5]:


student2 = Student('Elena', 'Ivanova', 'female')
student2.finished_courses += ['SQL']
student2.courses_in_progress += ['Java']
student2.grades['SQL'] = [8, 9, 10, 9, 10]
student2.grades['Java'] = [8, 9]


# In[6]:


student_list = [best_student, student2]


# #### Lecturers

# In[7]:


lecturer1 = Lecturer('Olga', 'Petrova')
lecturer1.courses_attached += ['Python']


# In[8]:


lecturer2 = Lecturer('Ivan', 'Smirnov')
lecturer2.courses_attached += ['Java']


# In[9]:


lecturer_list = [lecturer1, lecturer2]


# #### Reviewers

# In[10]:


reviewer1 = Reviewer('Alexander', 'Kozlov')
reviewer1.courses_attached += ['Python']


# In[11]:


reviewer2 = Reviewer('John', 'Smith')
reviewer2.courses_attached += ['Java']


# #### Оцениваем лекторов

# In[12]:


best_student.rate_lecturer(lecturer1, 'Python', 10)


# In[13]:


best_student.rate_lecturer(lecturer1, 'Java', 10)


# In[14]:


best_student.rate_lecturer(lecturer2, 'Python', 10)


# In[15]:


best_student.rate_lecturer(lecturer2, 'Java', 10)


# In[16]:


student2.rate_lecturer(lecturer1, 'Python', 10)


# In[17]:


student2.rate_lecturer(lecturer1, 'Java', 10)


# In[18]:


student2.rate_lecturer(lecturer2, 'Python', 10)


# In[19]:


student2.rate_lecturer(lecturer2, 'Java', 9)


# In[20]:


student2.rate_lecturer(lecturer2, 'Java', 7)


# In[21]:


best_student.rate_lecturer(lecturer1, 'Python', 9)


# #### Оцениваем студентов

# In[22]:


reviewer1.rate_hw(best_student, 'Python', 10)


# In[23]:


reviewer1.rate_hw(student2, 'Python', 10)


# In[24]:


reviewer1.rate_hw(best_student, 'Java', 10)


# In[25]:


reviewer1.rate_hw(student2, 'Java', 10)


# In[26]:


reviewer2.rate_hw(best_student, 'Python', 9)


# In[27]:


reviewer2.rate_hw(student2, 'Python', 9)


# In[28]:


reviewer2.rate_hw(best_student, 'Java', 9)


# In[29]:


reviewer2.rate_hw(student2, 'Java', 9)


# #### Перегружаем магический метод str у всех классов

# In[30]:


print(best_student)


# In[31]:


print(student2)


# In[32]:


print(lecturer1)


# In[33]:


print(lecturer2)


# In[34]:


print(reviewer1)


# In[35]:


print(reviewer2)


# In[36]:


best_student.__lt__(student2)


# In[37]:


student2.__lt__(best_student)


# In[40]:


student_list = [best_student, student2]

def medium_grade_student(student_list, course):
    """ Функция для подсчета средней оценки за домашние задания по всем студентам в рамках конкретного курса 
    (в качестве аргументов принимаем список студентов и название курса)
    """
    sum_grade = 0
    count_grade = 0
    for student in student_list:
        if course in student.grades:
            sum_grade += sum(student.grades[course])
            count_grade += len(student.grades[course])
    return sum_grade / count_grade

print(medium_grade_student(student_list, 'Python'))
print(medium_grade_student(student_list, 'Java'))


# In[41]:


lecturer_list = [lecturer1, lecturer2]

def medium_grade_lecturer(lecturer_list, course):
    """для подсчета средней оценки за лекции всех лекторов в рамках курса 
    (в качестве аргумента принимаем список лекторов и название курса)
    """
    sum_grade = 0
    count_grade = 0
    for lecturer in lecturer_list:
        if course in lecturer.grades:
            sum_grade += sum(lecturer.grades[course])
            count_grade += len(lecturer.grades[course])
    return sum_grade / count_grade

print(medium_grade_lecturer(lecturer_list, 'Python'))
print(medium_grade_lecturer(lecturer_list, 'Java'))

