import os
import re
import pickle

os.system('cls') or None


class Process:
    def __init__(self, pid):
        self.pid = pid

    def __str__(self):
        print(f'PID: {self.pid} ')

    def execute(self):
        pass

    def getPid(self):
        return self.pid

    def setPid(self, newPid):
        self.pid = newPid


class ComputingProcess(Process):
    def __init__(self, pid, expression, result=0, type=1):
        super().__init__(pid)
        self.expression = expression
        self.result = result
        self.type = type

    def __str__(self):
        print(f'PID: {self.pid}\n'
              f'Process Type: Computing Process\n'
              f'Expression: {self.expression}\n'
              f'Result: {self.execute()}\n')

    def execute(self):
        if '+' in self.expression:
            expression_separate = self.expression.strip().split('+')
            result = int(expression_separate[0]) + int(expression_separate[1])
            return result
        elif '-' in self.expression:
            expression_separate = self.expression.strip().split('-')
            result = int(expression_separate[0]) - int(expression_separate[1])
            return result
        elif '/' in self.expression:
            expression_separate = self.expression.strip().split('/')
            result = int(expression_separate[0]) / int(expression_separate[1])
            return result
        elif '*' in self.expression:
            expression_separate = self.expression.strip().split('*')
            result = int(expression_separate[0]) * int(expression_separate[1])
            return result
        else:
            return "You forgot the operator"

    def getExpression(self):
        return self.expression
    
    def getType(self):
        return self.type


class WritingProcess(Process):
    def __init__(self, pid, expression, type=2):
        super().__init__(pid)
        self.expression = expression
        self.type = type

    def __str__(self):
        print(f'PID: {self.pid}\n'
              f'Process Type: Writing Process\n'
              f'Expression: {self.expression}\n')

    def execute(self):
        if os.path.getsize('computing.txt') == 0:
            file = open('computing.txt', 'w')
            file.write(self.expression + '\n')
            file.close()
        else:
            file = open('computing.txt', 'a')
            file.write(self.expression + '\n')
            file.close()

    def getExpression(self):
        return self.expression

    def getType(self):
        return self.type


class ReadingProcess(Process):
    def __init__(self, pid, type=3):
        super().__init__(pid)
        self.type = type

    def __str__(self):
        print(f'PID: {self.pid}\n'
              f'Process Type: Reading Process\n')

    def execute(self):
        list_expression = []
        file = open('computing.txt', 'r')
        list_expression = file.readlines()
        for i in list_expression:
            computing_object = ComputingProcess(len(arrayProcess) + 1, i.rstrip())
            arrayProcess.append(computing_object)
        file.close()
        self.clearFile()

    def clearFile(self):
        file = open(f'computing.txt', 'w')
        file.write('')
        file.close()

    def getType(self):
        return self.type


class PrintingProcess(Process):
    def __init__(self, pid, type=4):
        super().__init__(pid)
        self.type = type

    def __str__(self):
        print(f'PID: {self.pid}\n'
              f'Process Type: Printing Process\n')

    def execute(self):
        for process in arrayProcess:
            process.__str__()
    
    def getType(self):
        return self.type


def expressionIsValid(expression):
    listExpression = re.split("[+]| /| [*]| -|", expression)
    listExpression.pop(0)
    listExpression.pop(1)
    listExpression.pop(2)
    if len(listExpression) == 2:
        return listExpression[0].strip().isnumeric() and listExpression[1].strip().isnumeric()
    else:
        return False


def menuCreateProcess():
    while True:
        print(f'[1] Computing Process\n'
              f'[2] Writing Process\n'
              f'[3] Reading Process\n'
              f'[4] Printing Process\n'
              f'[5] Voltar')
        option = int(input('Escolha a opção desejada: '))
        if option == 1:
            expression = str(input('Insira a expressão desejada: '))
            if expressionIsValid(expression):
                pid = len(arrayProcess) + 1
                object_computing = ComputingProcess(pid, expression)
                arrayProcess.append(object_computing)
            else:
                print('Expressão digitada é inválida')
        elif option == 2:
            expression = str(input('Insira a expressão desejada: '))
            pid = len(arrayProcess) + 1
            object_writing = WritingProcess(pid, expression)
            arrayProcess.append(object_writing)
        elif option == 3:
            pid = len(arrayProcess) + 1
            object_reading = ReadingProcess(pid)
            arrayProcess.append(object_reading)
        elif option == 4:
            pid = len(arrayProcess) + 1
            object_printing = PrintingProcess(pid)
            arrayProcess.append(object_printing)
        elif option == 5:
            mainMenu()
        else:
            print('Opção inválida')


def createProcess():
    while True:
        if len(arrayProcess) == 100:
            print('Limite máximo de processos em fila foi atingido')
        else:
            menuCreateProcess()


def executeProcess():
    if len(arrayProcess) > 0:
        if arrayProcess[0].getType() == 1:
            print(f'Expressão calculada: {arrayProcess[0].getExpression()}')
            print(f'Resultado: {arrayProcess[0].execute()}')
            arrayProcess.pop(0)
        elif arrayProcess[0].getType() == 2:
            print(f'Expressão registrada: {arrayProcess[0].getExpression()}')
            arrayProcess[0].execute()
            arrayProcess.pop(0)
        elif arrayProcess[0].getType() == 3:
            print('Expressões adicionadas a fila de execução.')
            arrayProcess[0].execute()
            arrayProcess.pop(0)
        elif arrayProcess[0].getType() == 4:
            arrayProcess[0].execute()
            arrayProcess.pop(0)
    else:
        print('Nenhum processo a ser executado em fila.')


def executeSpecificProcess():
    pid = int(input('Insira o PID do processo desejado: '))
    if pid > len(arrayProcess):
        print('PID inválido ')
    else:
        if arrayProcess[pid].getType() == 1:
            print(f'Expressão adicionada a fila: {arrayProcess[pid].getExpression()}')
            arrayProcess.pop(pid)
        elif arrayProcess[pid].getType() == 2:
            print(f'Expressão registrada: {arrayProcess[pid].getExpression()}')
            arrayProcess[pid].execute()
            arrayProcess.pop(pid)
        elif arrayProcess[pid].getType() == 3:
            print('Solicitação adicionada a fila de excecução')
            arrayProcess[pid].execute()
            arrayProcess.pop(pid)
        elif arrayProcess[pid].getType() == 4:
            print('Solicitação adicionada a fila de excecução')
            arrayProcess[pid].execute()
            arrayProcess.pop(pid)


def saveProcess():
    for object in arrayProcess:
        with open('process.txt', 'ab') as arquivo:
            pickle.dump(object, arquivo)


def loadProcess():
    with open("process.txt", 'rb') as arquivo:
        while True:
            try:
                obj = pickle.load(arquivo)
                arrayProcess.append(obj)
            except EOFError:
                break
    file = open('process.txt', 'w')
    file.write('')
    file.close()


def mainMenu():
    while True:
        print(f'Bem-vindo\n'
              f'[1] Criar processo\n'
              f'[2] Executar próximo\n'
              f'[3] Executar processo específico\n'
              f'[4] Salvar a fila de processos\n'
              f'[5] Carregar do arquivo a fila de processos\n'
              f'[6] Sair')
        option = int(input('Escolha a opção desejada: '))
        if option == 1:
            createProcess()
        elif option == 2:
            executeProcess()
        elif option == 3:
            executeSpecificProcess()
        elif option == 4:
            saveProcess()
        elif option == 5:
            loadProcess()
        elif option == 6:
            exit()
        else:
            print('Opção inválida')


if __name__ == '__main__':
    arrayProcess = []
    mainMenu()



