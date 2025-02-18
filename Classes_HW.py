#!/usr/bin/env python
# coding: utf-8

# #### Задание 1. Наследование
# 
# Исходя из квиза к предыдущему занятию, у нас уже есть класс преподавателей и класс студентов (вы можете взять этот код за основу или написать свой). Студентов пока оставим без изменения, а вот преподаватели бывают разные, поэтому теперь класс Mentor должен стать родительским классом, а от него нужно реализовать наследование классов Lecturer (лекторы) и Reviewer (эксперты, проверяющие домашние задания). Очевидно, имя, фамилия и список закрепленных курсов логично реализовать на уровне родительского класса. А чем же будут специфичны дочерние классы? Об этом в следующих заданиях.

# #### Задание 2. Атрибуты и взаимодействие классов.
# 
# В квизе к предыдущей лекции мы реализовали возможность выставлять студентам оценки за домашние задания. Теперь это могут делать только Reviewer (реализуйте такой метод). А что могут делать лекторы? Получать оценки за лекции от студентов :) Реализуйте метод выставления оценок лекторам у класса Student (оценки по 10-балльной шкале, хранятся в атрибуте-словаре у Lecturer, в котором ключи – названия курсов, а значения – списки оценок). Лектор при этом должен быть закреплен за тем курсом, на который записан студент.

# #### Задание № 3. Полиморфизм и магические методы
# 
# Перегрузите магический метод __str__ у всех классов.
# 
# У проверяющих он должен выводить информацию в следующем виде:
# print(some_reviewer)
# Имя: Some
# Фамилия: Buddy
# 
# У лекторов:
# print(some_lecturer)
# Имя: Some
# Фамилия: Buddy
# Средняя оценка за лекции: 9.9
# 
# А у студентов так:
# print(some_student)
# Имя: Ruoy
# Фамилия: Eman
# Средняя оценка за домашние задания: 9.9
# Курсы в процессе изучения: Python, Git
# Завершенные курсы: Введение в программирование
# 
# Реализуйте возможность сравнивать (через операторы сравнения) между собой лекторов по средней оценке за лекции и студентов по средней оценке за домашние задания.

# In[1]:


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
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'
    
    def student_avg_grade(self):
        """Метод расчета средней оценки за домашние задания по всем курсам """
        res = []
        for grade in self.grades.values():
            res.extend(grade)
            return float(sum(res) / len(res))
        
    def __str__(self):
        courses_in_progress_string = ', '.join(self.courses_in_progress)
        finished_courses_string = ', '.join(self.finished_courses)
        res = f'Имя: {self.name}\n' \
              f'Фамилия: {self.surname}\n' \
              f'Средняя оценка за домашние задания: {self.student_avg_grade()}\n' \
              f'Курсы в процессе изучения: {courses_in_progress_string}\n' \
              f'Завершенные курсы: {finished_courses_string}'
        return res

    
    
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
        res = []
        for grade in self.grades.values():
            res.extend(grade)
            return float(sum(res) / len(res))
        
    def __str__(self):
        return f' Имя: {self.name} \n Фамилия: {self.surname} \n Средняя оценка за лекции: {self.avg_grade()}'  

    


# Класс Reviewer наследует имя, фамилия и список закрепленные курсы от родительского класса Mentor.

class Reviewer(Mentor): #эксперты, проверяющие домашние задания
    def __init__(self, name, surname): 
        super().__init__(name, surname)
        
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


# #### Задание № 4. Полевые испытания
# 
# Создайте по 2 экземпляра каждого класса, вызовите все созданные методы, а также реализуйте две функции:
# 
# для подсчета средней оценки за домашние задания по всем студентам в рамках конкретного курса (в качестве аргументов принимаем список студентов и название курса);
# для подсчета средней оценки за лекции всех лекторов в рамках курса (в качестве аргумента принимаем список лекторов и название курса).

# #### Students

# In[2]:


# создадим по экземпляру наших классов и проверим содержимое атрибутов. 
# Добавим возможность хранить информацию студентов об оценках (словарь) и о списке курсов, которые сейчас изучаются.

best_student = Student('Ruoy', 'Eman', 'your_gender')
best_student.finished_courses += ['Git']
best_student.courses_in_progress += ['Python']
best_student.grades['Git'] = [10, 10, 10, 10, 10]
best_student.grades['Python'] = [10, 10]


# In[3]:


student2 = Student('Elena', 'Ivanova', 'female')
student2.finished_courses += ['SQL']
student2.courses_in_progress += ['Java']
student2.grades['SQL'] = [8, 9, 10, 9, 10]
student2.grades['Java'] = [8, 9]


# #### Lecturers

# In[4]:


lecturer1 = Lecturer('Olga', 'Petrova')
lecturer1.courses_attached += ['Python']


# In[5]:


lecturer2 = Lecturer('Ivan', 'Smirnov')
lecturer2.courses_attached += ['Java']


# #### Reviewers

# In[6]:


reviewer1 = Reviewer('Alexander', 'Kozlov')
reviewer1.courses_attached += ['Python']


# In[7]:


reviewer2 = Reviewer('John', 'Smith')
reviewer2.courses_attached += ['Java']


# #### Оцениваем лекторов

# In[8]:


best_student.rate_lecturer(lecturer1, 'Python', 10)


# In[9]:


best_student.rate_lecturer(lecturer1, 'Java', 10)


# In[10]:


best_student.rate_lecturer(lecturer2, 'Python', 10)


# In[11]:


best_student.rate_lecturer(lecturer2, 'Java', 10)


# In[12]:


student2.rate_lecturer(lecturer1, 'Python', 10)


# In[13]:


student2.rate_lecturer(lecturer1, 'Java', 10)


# In[14]:


student2.rate_lecturer(lecturer2, 'Python', 10)


# In[15]:


student2.rate_lecturer(lecturer2, 'Java', 9)


# In[16]:


student2.rate_lecturer(lecturer2, 'Java', 7)


# In[17]:


best_student.rate_lecturer(lecturer1, 'Python', 9)


# #### Оцениваем студентов

# In[18]:


reviewer1.rate_hw(best_student, 'Python', 10)


# In[19]:


reviewer1.rate_hw(student2, 'Python', 10)


# In[20]:


reviewer1.rate_hw(best_student, 'Java', 10)


# In[21]:


reviewer1.rate_hw(student2, 'Java', 10)


# In[22]:


reviewer2.rate_hw(best_student, 'Python', 9)


# In[23]:


reviewer2.rate_hw(student2, 'Python', 9)


# In[24]:


reviewer2.rate_hw(best_student, 'Java', 9)


# In[25]:


reviewer2.rate_hw(student2, 'Java', 9)


# #### Перегружаем магический метод str у всех классов

# In[26]:


print(best_student)


# In[27]:


print(student2)


# In[28]:


print(lecturer1)


# In[29]:


print(lecturer2)


# In[30]:


print(reviewer1)


# In[31]:


print(reviewer2)


# In[32]:


from functools import total_ordering

@total_ordering

class Student:    
    def __lt__(self, other): 
        """Создаём метод, который сравнивает (через оператор сравнения <=) между собой студентов по средней оценке 
        за домашние задания.""" 
        if not isinstance(other, Student): 
            print('Невозможно сравнить!') 
        return self.student_avg_grade() < other.student_avg_grade()
    
    def __gt__(self, other): 
        """Создаём метод, который сравнивает (через операторы сравнения >=) между собой студентов по средней оценке 
        за домашние задания.""" 
        if not isinstance(other, Student): 
            print('Невозможно сравнить!') 
        return self.student_avg_grade() > other.student_avg_grade()
    


# In[33]:


@total_ordering
class Lecturer(Mentor):
    def __lt__(self, other): 
        """Создаём метод, который сравнивает (через оператор сравнения <=) между собой лекторов по средней оценке 
        от студентов.""" 
        if not isinstance(other, Student): 
            print('Невозможно сравнить!') 
        return self.avg_grade() < other.avg_grade()
    
    def __gt__(self, other): 
        """Создаём метод, который сравнивает (через операторы сравнения >=) между собой лекторов по средней оценке 
        от студентов.""" 
        if not isinstance(other, Student): 
            print('Невозможно сравнить!') 
        return self.avg_grade() > other.avg_grade()


# In[34]:


best_student.__lt__(student2)


# In[35]:


student2.__lt__(best_student)


# In[36]:


best_student.__gt__(student2)


# In[37]:


student2.__gt__(best_student)

