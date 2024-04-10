import copy


class SelfReferencingEntity:
    def __init__(self):
        self.parent = None

    def set_parent(self, parent):
        self.parent = parent


class SomeComponent:
    """
    파이썬은 `copy.copy` 및 `copy.deepcopy` 함수를 통한 자체 프로토타입 인터페이스를 제공합니다.
    사용자 정의 구현을 하려면 `__copy__` 및 `__deepcopy__` 멤버 함수를 오버라이드해야 합니다.
    """

    def __init__(self, some_int, some_list_of_objects, some_circular_ref):
        self.some_int = some_int
        self.some_list_of_objects = some_list_of_objects
        self.some_circular_ref = some_circular_ref

    def __copy__(self):
        """
        얕은 복사를 생성합니다. 이 메서드는 누군가가 이 객체와 함께 `copy.copy`를 호출할 때마다 호출됩니다.
        반환된 값은 새로운 얕은 복사본으로 반환됩니다.
        """

        # 먼저 중첩된 객체의 복사본을 만듭니다.
        some_list_of_objects = copy.copy(self.some_list_of_objects)
        some_circular_ref = copy.copy(self.some_circular_ref)

        # 그런 다음 준비된 중첩된 객체의 복사본을 사용하여 객체 자체를 복제합니다.
        new = self.__class__(
            self.some_int, some_list_of_objects, some_circular_ref
        )
        new.__dict__.update(self.__dict__)

        return new

    def __deepcopy__(self, memo=None):
        """
        깊은 복사를 생성합니다. 이 메서드는 누군가가 이 객체와 함께 `copy.deepcopy`를 호출할 때마다 호출됩니다.
        반환된 값은 새로운 깊은 복사본으로 반환됩니다.

        `memo` 인자의 사용은 무엇인가요? `memo`는 원형 참조 인스턴스에서 무한 재귀 복사를 방지하기 위해
        `deepcopy` 라이브러리에서 사용되는 사전입니다. `__deepcopy__` 구현에서 모든 `deepcopy` 호출에
        이를 전달하여 무한 재귀를 방지합니다.
        """
        if memo is None:
            memo = {}

        # 먼저 중첩된 객체의 복사본을 만듭니다.
        some_list_of_objects = copy.deepcopy(self.some_list_of_objects, memo)
        some_circular_ref = copy.deepcopy(self.some_circular_ref, memo)

        # 그런 다음 준비된 중첩된 객체의 복사본을 사용하여 객체 자체를 복제합니다.
        new = self.__class__(
            self.some_int, some_list_of_objects, some_circular_ref
        )
        new.__dict__ = copy.deepcopy(self.__dict__, memo)

        return new


if __name__ == "__main__":

    list_of_objects = [1, {1, 2, 3}, [1, 2, 3]]
    circular_ref = SelfReferencingEntity()
    component = SomeComponent(23, list_of_objects, circular_ref)
    circular_ref.set_parent(component)

    shallow_copied_component = copy.copy(component)

    # shallow_copied_component의 리스트를 변경하고, component에도 변경이 반영되는지 확인합니다.
    shallow_copied_component.some_list_of_objects.append("another object")
    if component.some_list_of_objects[-1] == "another object":
        print(
            "`shallow_copied_component`의 some_list_of_objects에 요소를 추가하면 "
            "`component`의 some_list_of_objects에도 추가됩니다."
        )
    else:
        print(
            "`shallow_copied_component`의 some_list_of_objects에 요소를 추가하면 "
            "`component`의 some_list_of_objects에 추가되지 않습니다."
        )

    # 리스트 안의 집합을 변경해봅니다.
    component.some_list_of_objects[1].add(4)
    if 4 in shallow_copied_component.some_list_of_objects[1]:
        print(
            "`component`의 some_list_of_objects 내의 객체를 변경하면 "
            "`shallow_copied_component`의 some_list_of_objects 내의 해당 객체도 변경됩니다."
        )
    else:
        print(
            "`component`의 some_list_of_objects 내의 객체를 변경하면 "
            "`shallow_copied_component`의 some_list_of_objects 내의 해당 객체도 변경되지 않습니다."
        )

    deep_copied_component = copy.deepcopy(component)

    # deep_copied_component의 리스트를 변경하고, component에도 변경이 반영되는지 확인합니다.
    deep_copied_component.some_list_of_objects.append("one more object")
    if component.some_list_of_objects[-1] == "one more object":
        print(
            "`deep_copied_component`의 some_list_of_objects에 요소를 추가하면 "
            "`component`의 some_list_of_objects에도 추가됩니다."
        )
    else:
        print(
            "`deep_copied_component`의 some_list_of_objects에 요소를 추가하면 "
            "`component`의 some_list_of_objects에 추가되지 않습니다."
        )

    # 리스트 안의 집합을 변경해봅니다.
    component.some_list_of_objects[1].add(10)
    if 10 in deep_copied_component.some_list_of_objects[1]:
        print(
            "`component`의 some_list_of_objects 내의 객체를 변경하면 "
            "`deep_copied_component`의 some_list_of_objects 내의 해당 객체도 변경됩니다."
        )
    else:
        print(
            "`component`의 some_list_of_objects 내의 객체를 변경하면 "
            "`deep_copied_component`의 some_list_of_objects 내의 해당 객체도 변경되지 않습니다."
        )

    print(
        f"id(deep_copied_component.some_circular_ref.parent): "
        f"{id(deep_copied_component.some_circular_ref.parent)}"
    )
    print(
        f"id(deep_copied_component.some_circular_ref.parent.some_circular_ref.parent): "
        f"{id(deep_copied_component.some_circular_ref.parent.some_circular_ref.parent)}"
    )
    print(
        "^^ 이것은 deepcopy된 객체가 동일한 참조를 가지고 있음을 보여주며, 반복적으로 복제되지 않았음을 나타냅니다."
    )
