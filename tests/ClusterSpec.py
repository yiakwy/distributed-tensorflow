
clusters = {
'local': ["localhost:9001", "localhost:9002"],
'docker-local': ["localhost:4000", "localhost:4001"]
}
job_name = "local"
task_indice = [0, 1]
tasks_gen = iter(task_indice)
taskPoolSize = 2
