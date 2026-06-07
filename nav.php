<nav class="bg-[#111827] px-6 py-4 sticky top-0 z-50">
    <div class="flex items-center justify-between">
    
    <h1 class="text-xl text-lime-400 font-bold"><a href="index.php">Kallam Samad</a></h1>
        <ul class="hidden md:flex gap-8 items-center">
            <li><a class="hover:text-lime-400 transition-colors" href="aboutme.php">About Me</a></li>
            <li><a class="hover:text-lime-400 transition-colors" href="projects.php">Projects</a></li>
            <li><a class="hover:text-lime-400 transition-colors" href="contact.php">Contact</a></li>
            <li><a class="hover:text-lime-400 transition-colors" href="resume.php">Resume</a></li>
        </ul>

        <!-- Right side: pfp + hamburger -->
        <div class="flex flex items-center justify-end gap-2">
            <img src="Images/pfp.jpg" alt="Profile picture" class="rounded-full h-12 w-12 object-cover">
            <button class="md:hidden text-white text-2xl" onclick="toggleMenu()"><div class="hamburger text-3xl transition-transform duration-300">☰</div></button>
        </div>
    </div>

    <!-- Mobile menu -->
    <div id="mobile-menu" class=" animate-fade-in-down hidden flex-col gap-0 m-0 pt-4 md:hidden">
        <a class="hover:text-white bg-lime-600 border-12 border-lime-600 hover:bg-lime-600 transition-colors block" href="index.php">Home</a>
        <a class="hover:text-white border-8 border-[#111827] hover:bg-lime-600 hover:border-lime-600 transition-colors block" href="aboutme.php">About Me</a>
        <a class="hover:text-white border-8 border-[#111827] hover:bg-lime-600 hover:border-lime-600 transition-colors block" href="projects.php">Projects</a>
        <a class="hover:text-white border-8 border-[#111827] hover:bg-lime-600 hover:border-lime-600 transition-colors block" href="contact.php">Contact</a>
        <a class="hover:white border-8 border-[#111827] hover:bg-lime-600 hover:border-lime-600 transition-colors block" href="resume.php">Resume</a>
    </div>
</nav>

<script>
  
function toggleMenu() {
    const menu = document.getElementById('mobile-menu');
    const hamburger=document.querySelector(".hamburger");
    menu.classList.toggle('hidden');
    menu.classList.toggle('flex');
    hamburger.classList.toggle("rotate-[90deg]");


}
 
</script>