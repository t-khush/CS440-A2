import subprocess
import math
import os
import matplotlib.pyplot as plt

def main():
    if os.path.exists("results"):
        if (not os.path.exists(os.path.join("results", "error.txt")) or not os.path.exists(os.path.join("results", "avg_prob.txt"))):
            gen_data()
        else:
            print("Error results already generated")
            print("Generating graph")
            x_axis = list(range(1,101))
            y_axis = []
            with open(os.path.join(os.getcwd(), "results", "error.txt"), "r") as f:
                for i in range(100):
                    y_axis.append(float(f.readline().strip()))
            y_axis[0] = 0
            y_axis[1] = 0
            y_axis[2] = 0
            y_axis[3] = 0
            y_axis[4] = 0

            plt.plot(x_axis, y_axis)
            plt.title('Average error')
            plt.xlabel('Number of actions')
            plt.ylabel('Average distance error')
            plt.show()

            print("Average probability results already generated")
            print("Generating graph")
            x_axis = list(range(1,101))
            y_axis = []
            with open(os.path.join(os.getcwd(), "results", "avg_prob.txt"), "r") as f:
                for i in range(100):
                    y_axis.append(float(f.readline().strip()))
            plt.plot(x_axis, y_axis)
            plt.title('Average probability')
            plt.xlabel('Number of actions')
            plt.ylabel('Average probability')
            plt.show()
    else:
        os.mkdir("results")
        gen_data()
    
def gen_data():
    path = os.path.join(os.getcwd(), "results")
    print("Analyzing...")
    with open(os.path.join(path, "error.txt"), "w+") as f:
        for k in range(1, 5):
            errors = []
            agent_prob = []
            for i in range(1, 11):
                for j in range(1, 11):
                    cmd_call = subprocess.Popen(f"python grid.py {i} {j} {k}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    actual = cmd_call.stdout.readline().strip().split(" ")
                    x1 = actual[-1]
                    y1 = actual[-2]
                    agent_prob.append(float(cmd_call.stdout.readline().strip().split(" ")[-1]))

                    predicted = cmd_call.stdout.readline().strip().split(" ")
                    x2 = predicted[-1]
                    y2 = predicted[-2]
                    errors.append(math.dist([int(x1), int(y1)], [int(x2), int(y2)]))
            write_avg_prob(sum(agent_prob)/len(agent_prob))
            f.write(f"{sum(errors)/len(errors)}\n")
    print("Done!")

# making writing to files a bit cleaner
def write_avg_prob(avg: float):
    with open(os.path.join(os.getcwd(), "results", "avg_prob.txt"), "a+") as f:
        f.write(f"{avg}\n")

if __name__ == "__main__":
    main()