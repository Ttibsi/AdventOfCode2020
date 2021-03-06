# pt2: Fix the program so that it terminates normally by changing exactly one
# NOP to JMP or reverse. What is the value of the accumulator after the program
# terminates.
import copy


def repairInstructionSet(
    instructionSet: list[str], changedIndex: int
) -> tuple[list[str], int]:

    newInstructions = copy.deepcopy(instructionSet)

    for index, instruction in enumerate(newInstructions):
        if index <= changedIndex:
            continue
        elif instruction[:3] == "jmp" and index > changedIndex:
            newInstructions[index] = instruction.replace("jmp", "nop")
            changedIndex = index
            break
        elif instruction[:3] == "nop" and index > changedIndex:
            newInstructions[index] = instruction.replace("nop", "jmp")
            changedIndex = index
            break
        else:
            continue

    return newInstructions, changedIndex


def bufChecker(
    bufHistory: list[int], instruction: tuple[int, str]
) -> tuple[bool, list[int]]:
    instructionPointer = instruction[0]

    if instructionPointer in bufHistory:
        return True, bufHistory
    else:
        return False, bufHistory


def interpreter(instructionSet: list[str]) -> tuple[bool, int]:
    accumulator: int = 0
    bufHistory: list[int] = []
    pointer: int = 0

    instructionsWithPointers: list[tuple[int, str]] = [
        (i, v.rstrip()) for i, v in enumerate(instructionSet)
    ]

    while pointer < len(instructionsWithPointers):
        instruction: tuple[int, str] = instructionsWithPointers[pointer]

        # print(
        #    f"Pointer: {pointer},",
        #    f"instruction: {instruction},",
        #    f"accumulator: {accumulator}",
        # )

        alreadyExecuted, bufHistory = bufChecker(bufHistory, instruction)

        if alreadyExecuted:
            return False, accumulator
        else:
            bufHistory.append(instruction[0])

        if instruction[1][:3] == "jmp":
            pointer += int(instruction[1][4:])
        else:
            pointer += 1
            if instruction[1][:3] == "acc":
                accumulator += int(instruction[1][4:])

    return True, accumulator


def main(filename: str) -> int:
    with open(filename) as rawInstructions:
        instructionSet = rawInstructions.readlines()

    changedIndex: int = 0
    successfulExecutionFlag: bool = False

    while not successfulExecutionFlag:
        print(f"{instructionSet=}")
        repairedInstructions, changedIndex = repairInstructionSet(
            instructionSet, changedIndex
        )

        # print(
        #    f"Repaired instruction: {repairedInstructions[changedIndex][:-1]}",
        #    f"at index {changedIndex}",
        # )

        successfulExecutionFlag, accumulator = interpreter(repairedInstructions)

        if changedIndex > len(instructionSet):
            break

    if successfulExecutionFlag:
        print(f"{accumulator=}")
    else:
        print("Instruction repair failed")

    return 0


if __name__ == "__main__":
    raise SystemExit(main("SuppliedInputs/day8.txt"))
