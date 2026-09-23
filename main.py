from src.model import GradeConverterModel
from src.view import GradeConverterView
from src.controller import GradeConverterController

if __name__ == "__main__":
    model = GradeConverterModel()
    view = GradeConverterView()
    controller = GradeConverterController(model, view)
    view.mainloop()