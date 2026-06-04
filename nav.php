<nav class="bg-[#111827] px-6 py-4">
    <div class="flex items-center justify-between">
        <ul class="hidden md:flex gap-8 items-center">
            <h1 class="text-xl text-lime-400 font-bold">Kallam Samad</h1>
            <li><a class="hover:text-lime-400 transition-colors" href="aboutme.php">About Me</a></li>
            <li><a class="hover:text-lime-400 transition-colors" href="projects.php">Projects</a></li>
            <li><a class="hover:text-lime-400 transition-colors" href="contact.php">Contact</a></li>
            <li><a class="hover:text-lime-400 transition-colors" href="resume.php">Resume</a></li>
        </ul>

        <!-- Right side: pfp + hamburger -->
        <div class="flex flex items-center justify-end gap-4">
            <img src="Images/pfp.jpg" alt="Profile picture" class="rounded-full h-12 w-12 object-cover">
            <button class="md:hidden text-white text-2xl" onclick="toggleMenu()">☰</button>
        </div>
    </div>

    <!-- Mobile menu -->
    <div id="mobile-menu" class="hidden flex-col gap-4 pt-4 md:hidden">
        <a class="hover:text-lime-400 transition-colors block" href="aboutme.php">About Me</a>
        <a class="hover:text-lime-400 transition-colors block" href="projects.php">Projects</a>
        <a class="hover:text-lime-400 transition-colors block" href="contact.php">Contact</a>
        <a class="hover:text-lime-400 transition-colors block" href="resume.php">Resume</a>
    </div>
</nav>

<script>
function toggleMenu() {
    const menu = document.getElementById('mobile-menu');
    menu.classList.toggle('hidden');
    menu.classList.toggle('flex');
}
</script>