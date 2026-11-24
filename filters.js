const filterGroup = document.querySelector('.filters');
const filters = [...filterGroup.querySelectorAll('button')];
const groups = [...document.querySelectorAll('[data-group]')];
const count = document.getElementById('project-count');
const isChinese = document.documentElement.lang === 'zh-CN';

filterGroup.hidden = false;
filterGroup.addEventListener('click', (event) => {
  const selected = event.target.closest('button[data-filter]');
  if (!selected) return;

  const category = selected.dataset.filter;
  for (const button of filters) {
    button.setAttribute('aria-pressed', String(button === selected));
  }
  let visible = 0;
  for (const group of groups) {
    group.hidden = category !== 'all' && category !== group.dataset.group;
    if (!group.hidden) visible += group.querySelectorAll('.project').length;
  }
  count.textContent = isChinese ? `${visible} 个项目` : `${visible} ${visible === 1 ? 'project' : 'projects'}`;
});
