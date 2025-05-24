buildscript {
    repositories {
        google()
        jcenter()
    }
    dependencies {
        classpath("com.google.gms:google-services:4.4.2") // ✅ Correct version path
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

// Optional custom build directory logic (remove if not needed)
val newBuildDir = rootProject.layout.buildDirectory.dir("../../build").get()
rootProject.layout.buildDirectory.set(newBuildDir)

subprojects {
    val newSubprojectBuildDir = newBuildDir.dir(project.name)
    project.layout.buildDirectory.set(newSubprojectBuildDir)
    project.evaluationDependsOn(":app")
}

tasks.register<Delete>("clean") {
    delete(rootProject.layout.buildDirectory)
}



// buildscript {
//     repositories {
//         google()
//         jcenter()
//     }

//     dependencies {
//         classpath("com.google.gms.google-services:4.4.2")
//     }
// }

// allprojects {
//     repositories {
//         google()
//         mavenCentral()
//     }
// }

// val newBuildDir: Directory = rootProject.layout.buildDirectory.dir("../../build").get()
// rootProject.layout.buildDirectory.value(newBuildDir)

// subprojects {
//     val newSubprojectBuildDir: Directory = newBuildDir.dir(project.name)
//     project.layout.buildDirectory.value(newSubprojectBuildDir)
// }
// subprojects {
//     project.evaluationDependsOn(":app")
// }

// tasks.register<Delete>("clean") {
//     delete(rootProject.layout.buildDirectory)
// }
