class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type,
                 duration,
                 distance,
                 speed,
                 calories
                 ) -> None:
        self.training = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        message: str = (f'Тип тренировки: {self.training}; '
                        f'Длительность: {self.duration:.3f} ч.; '
                        f'Дистанция: {self.distance:.3f} км; '
                        f'Ср. скорость: {self.speed:.3f} км/ч; '
                        f'Потрачено ккал: {self.calories:.3f}.'
                        )
        return message


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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message_object: InfoMessage = InfoMessage(self.__class__.__name__,
                                                  self.duration,
                                                  self.get_distance(),
                                                  self.get_mean_speed(),
                                                  self.get_spent_calories())
        return message_object


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        super().get_distance
        super().get_mean_speed
        super().show_training_info

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
                 ) * self.weight
                / Training.M_IN_KM
                * self.duration
                * Training.MINUTE_IN_HOUR
                )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER_1: float = 0.035
    CCALORIES_WEIGHT_MULTIPLIER_2: float = 0.029
    TRANSFORM_MS_TO_KMH: float = 0.278

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        self.height = height
        super().__init__(action, duration, weight)
        super().get_distance
        super().get_mean_speed
        super().show_training_info

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_WEIGHT_MULTIPLIER_1
                 * self.weight
                 + ((self.get_mean_speed()
                     / self.TRANSFORM_MS_TO_KMH) ** 2
                    / self.height)
                 * self.CCALORIES_WEIGHT_MULTIPLIER_2 * self.weight
                 )
                * self.duration * Training.MINUTE_IN_HOUR
                )


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
        super().show_training_info

    def get_distance(self) -> float:
        """Формула расчсёта дистнации для плавания"""
        return self.action * self.LEN_STEP / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Формула расчёта средней скорости при плавании"""
        return (self.length_pool
                * self.count_pool
                / Training.M_IN_KM
                / self.duration
                )

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                + self.CALORIES_SPEED_MULTIPLIER
                 ) * self.CALORIES_MULTIPLIER
                * self.weight * self.duration
                )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    workout_types = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking
                     }

    return workout_types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
