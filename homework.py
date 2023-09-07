from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MINUTE_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения, км/ч."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError("Необходимо переопределить метод")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
                 ) * self.weight
                / self.M_IN_KM
                * self.duration
                * self.MINUTE_IN_HOUR
                )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER_1: float = 0.035
    CCALORIES_WEIGHT_MULTIPLIER_2: float = 0.029
    TRANSFORM_MS_TO_KMH: float = 0.278
    CONVERT_СM_TO_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        self.height = height
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_WEIGHT_MULTIPLIER_1
                * self.weight
                + ((self.get_mean_speed() * self.TRANSFORM_MS_TO_KMH) ** 2
                   / (self.height / self.CONVERT_СM_TO_M))
                * self.CCALORIES_WEIGHT_MULTIPLIER_2
                * self.weight)
                * (self.duration * self.MINUTE_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""
    CALORIES_SPEED_MULTIPLIER: float = 1.1
    LEN_STEP: float = 1.38
    CALORIES_MULTIPLIER: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Формула расчсёта дистнации для плавания"""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Формула расчёта средней скорости при плавании"""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration
                )

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                + self.CALORIES_SPEED_MULTIPLIER
                 ) * self.CALORIES_MULTIPLIER
                * self.weight * self.duration
                )


def read_package(workout_class: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_classes: dict = {'SWM': Swimming,
                             'RUN': Running,
                             'WLK': SportsWalking}
    if workout_class not in workout_classes:
        raise Exception("Не верный тип тренировки " + workout_class)

    else:
        return workout_classes[workout_class](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: tuple[str, list[int]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        try:
            training = read_package(workout_type, data)
            main(training)
        except TypeError:
            print('Ошибка в пакете данных ' + workout_type)
